import annotationlib
from collections.abc import Generator
from typing import Any, get_args

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import core_schema

_validate_subclass_users: set[type[BaseModel]] = set()


def uses_validate_subclasses_field(cls: type[BaseModel]):
    """Decorator that registers a class as using a `ValidateSubclass` field validator and thus schedules it for rebuilding on demand."""
    _validate_subclass_users.add(cls)
    return cls


def rebuild_validate_subclasses_models():
    """Force rebuilds of all models previously registered with `@uses_validate_subclass_field`."""
    for m in _validate_subclass_users:
        m.model_rebuild(force=True)


def _get_subclasses_recursively(cls: type, yield_self=False) -> Generator[type]:
    if yield_self:
        yield cls

    subclasses = cls.__subclasses__()
    yield from subclasses

    for sc in subclasses:
        yield from _get_subclasses_recursively(sc, False)


class ValidateSubclasses:
    """Validator annotation to a pydantic model field that dynamically constructs a discriminated union out of all subclasses of the given type (and also subsubclasses etc.).

    Remember to add the `@uses_validate_subclass_field` decorator to the class containing a field using this validator to be able to rebuild the model when new subclasses are added."""

    def __init__(self, base_type: type[BaseModel], allow_base=True):
        """
        Args:
            base_type (type[BaseModel]): the type from which to dive into the subclass hierarchy
            allow_base (bool): whether to include the `base_type` itself in the generated union
        """
        self.base_type = base_type
        self.allow_base = allow_base

    def __get_pydantic_core_schema__(
        self,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.tagged_union_schema(
            {
                t: handler.generate_schema(sc)
                for sc in _get_subclasses_recursively(self.base_type, self.allow_base)
                for t in get_args(annotationlib.get_annotations(sc)["type"])
            },
            discriminator="type",
        )
