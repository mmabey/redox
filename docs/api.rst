API
===

Factory
-------

.. autofunction:: redox.factory.redox_object_factory

.. autofunction:: redox.factory.from_redox_to_generic

Base classes
------------

.. autoclass:: redox.abstract_base.RedoxAbstractModel
   :members: cast_from, model_dump, model_dump_json
   :member-order: bysource

.. autoclass:: redox.abstract_base.EventTypeAbstractModel
   :show-inheritance:

.. autoclass:: redox.abstract_base.GenericEventTypeAbstractModel
   :members: to_redox, redox_dict, redox_json
   :show-inheritance:

.. autofunction:: redox.abstract_base.lenient_ingest

.. autoexception:: redox.abstract_base.CannotRectifyValidationError
   :show-inheritance:
