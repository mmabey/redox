Changelog
=========

2.0.0 (2026-09-06)
------------------

First release under the ``redox`` name (previously ``pyredox``) and the first to
target Pydantic v2. This is a major release with breaking changes.

Breaking
~~~~~~~~

- **Package renamed** ``pyredox`` -> ``redox``. Update imports:
  ``from redox.patientadmin.newpatient import NewPatient``. The ``pyredox``
  listing on PyPI is frozen at ``1.0.4``.
- **Pydantic v2 required** (``pydantic>=2.11``). Model APIs follow v2:
  ``model_dump()`` / ``model_dump_json()`` / ``model_validate()`` /
  ``model_rebuild()``.
- **Minimum Python is now 3.11** (was 3.7).
- ``.dict()`` and ``.json()`` still work but emit a ``DeprecationWarning`` and
  delegate to ``model_dump()`` / ``model_dump_json()``. On generic models they
  first convert to the "proper Redox" model, as before.
- Field names are **bare again** (``obj.Meta.DataModel``), matching ``pyredox``
  1.0.4. The interim ``Meta_`` / ``DataModel_`` convention from the abandoned v2
  branch is gone.
- ``redox.generic.types`` classes are now defined privately (``_Address``) with a
  public alias (``Address = _Address``) to satisfy Pydantic v2's field/type
  name-clash rule. ``redox.generic.types.Address`` and ``isinstance`` checks are
  unaffected.
- Data models Redox has retired are no longer generated: ``claim/submission``,
  ``claim/payment``, ``enrichment/naturallanguageprocessing*``.

Added
~~~~~

- ``redox.lenient_ingest()`` context manager and
  ``redox_object_factory(payload, lenient=True)`` — parse payloads that contain
  fields the installed schema version doesn't know about (e.g. a Redox schema
  addition) by dropping the unknown keys instead of raising. Outbound validation
  is unchanged.
- Numeric values are accepted for schema-typed string fields again
  (``coerce_numbers_to_str``), restoring v1 leniency.
- ``py.typed`` marker; the package ships type information.

Changed
~~~~~~~

- Tooling modernised: uv, ``uv_build``, ruff (lint + format), PEP 621 packaging,
  Read the Docs. Generation, testing, and publishing run through
  `gen_redox_lib <https://github.com/mmabey/gen_redox_lib>`_.
