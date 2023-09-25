# -*- coding: utf-8 -*-
"""Base class for all Redox elements."""
import abc
from typing import Any, Mapping, Union

from pydantic import BaseModel, Field, ValidationError

__all__ = [
    "CannotRectifyValidationError",
    "EventTypeAbstractModel",
    "GenericEventTypeAbstractModel",
    "MetaBase",
    "RedoxAbstractModel",
]


class CannotRectifyValidationError(Exception):
    """Raised when cast_from can't autocorrect a ValidationError."""


def _pop_offending_field_values(
    args_for_new_object: dict, validation_err: ValidationError
):
    for err in validation_err.errors():
        if err["type"] != "extra_forbidden":
            raise CannotRectifyValidationError(
                f"Unknown validation error type: {err['type']}"
            )

        parent_of_offending_field = args_for_new_object
        locations = list(err["loc"])
        offending_field = locations.pop()
        traversed = []
        for field in locations:
            # Note: It's currently unclear if this loop will ever be used. It wasn't in
            # tests, but since loc_tuple() is always a tuple, we're erring on the side
            # of caution by leaving this here. But it's also unclear how to test the
            # loop operations properly.
            next_in_loc = parent_of_offending_field.get(field, None)
            if not next_in_loc:
                raise CannotRectifyValidationError(
                    f"Cannot traverse path to offending field: "
                    f"{'->'.join(traversed) if traversed else 'Object'} doesn't have "
                    f'a field called "{field}".'
                )
            traversed.append(field)
            parent_of_offending_field = next_in_loc

        try:
            parent_of_offending_field.pop(offending_field)
        except KeyError as err:
            raise CannotRectifyValidationError(
                f"Cannot traverse path to offending field: "
                f"{'->'.join(traversed) if traversed else 'Object'} doesn't have "
                f'a field called "{offending_field}".'
            ) from err


class RedoxAbstractModel(BaseModel, abc.ABC, extra="forbid"):
    Extensions: Any = Field(None)

    @classmethod
    def cast_from(
        cls, *others: Union["RedoxAbstractModel", Mapping]
    ) -> "RedoxAbstractModel":
        """Create a new redox object from the passed object(s).

        Intended for use when you need to assign the same values to multiple
        objects while avoiding any type-checking errors. For example, on a
        generic ``Visit`` object, there are multiple provider fields that only
        differ in which role that provider filled for the visit. If the same
        provider filled multiple roles, it is redundant to specify the same
        provider information in multiple object instances.

        Using this ``cast_from`` class method, you only need to create a
        generic object with all the provider information and then cast it to
        the different types::

            provider = AdmittingProvider(...)
            visit = Visit(
                AdmittingProvider=provider,
                AttendingProvider=AttendingProvider.cast_from(provider),
                VisitProvider=VisitProvider.cast_from(provider),
            )

        If multiple objects are passed to ``cast_from``, the first object's
        fields will be given preference, then the second object's fields, and
        so on. This mimics the MRO for multiple inheritance (see
        https://docs.python.org/3/tutorial/classes.html#multiple-inheritance
        for more info).
        """

        # Gather all arguments for creating the new object into a single dictionary by
        # starting with an empty dict then `update()`ing it using the dict version of
        # each object in ``others``.
        others = [
            other.model_dump() if hasattr(other, "model_dump") else dict(other)
            for other in reversed(others)
        ]
        args = {}
        for other in others:
            args.update(other)

        new_object = None
        while new_object is None:
            try:
                new_object = cls(**args)
            except ValidationError as err:
                _pop_offending_field_values(args, err)

        return new_object

    def dict(self, *_, **__):
        raise DeprecationWarning(
            "The `dict` method is deprecated; use `model_dump` instead."
        )

    def json(self, *_, **__):
        raise DeprecationWarning(
            "The `json` method is deprecated; use `model_dump_json` instead."
        )

    def model_dump(
        self,
        *,
        mode="python",
        include=None,
        exclude=None,
        by_alias: bool = True,  # Differs from default
        exclude_unset: bool = True,  # Differs from default
        exclude_defaults: bool = False,
        exclude_none: bool = True,  # Differs from default
        round_trip: bool = False,
        **kwargs,
    ):
        return super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            **kwargs,
        )


class MetaBase(RedoxAbstractModel, abc.ABC):
    """Bare minimum fields for all ``Meta`` types."""

    DataModel_: str = Field(..., alias="DataModel")
    EventType_: str = Field(..., alias="EventType")


class EventTypeAbstractModel(RedoxAbstractModel, abc.ABC):
    """Event types should inherit from this instead of RedoxAbstractModel."""

    Meta_: MetaBase = Field(..., alias="Meta")


class GenericEventTypeAbstractModel(RedoxAbstractModel):
    _redox_module: Any = ...  # e.g. patientadmin
    Meta_: MetaBase = Field(..., alias="Meta")

    def to_redox(self) -> RedoxAbstractModel:
        """Figure out the correct redox model, instantiate, and return."""

        class_name = type(self).__name__

        event_module = getattr(self._redox_module, class_name.lower())
        if not event_module:
            raise AttributeError(
                f"Couldn't find Redox event module for {class_name.lower()}"
            )

        event_class = getattr(event_module, class_name)
        if not event_class:
            raise AttributeError(f"Couldn't find Redox event class for {class_name}")

        return event_class.model_validate(super().model_dump())

    def dict(self):
        raise DeprecationWarning(
            "The `dict` method is deprecated; use `redox_dict` or `model_dump` instead."
        )

    def json(self):
        raise DeprecationWarning(
            "The `json` method is deprecated; use `redox_json` or `model_dump_json` "
            "instead."
        )

    def redox_dict(self, *args, **kwargs):
        return self.to_redox().model_dump(*args, **kwargs)

    def redox_json(self, *args, **kwargs):
        return self.to_redox().model_dump_json(*args, **kwargs)
