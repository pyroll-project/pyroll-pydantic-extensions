from typing import Annotated, Any, get_args, get_origin

import numpy as np
from pydantic import GetCoreSchemaHandler, PlainSerializer, ValidateAs
from pydantic_core import core_schema


class ArrayValidator:
    """After validator that checks the runtime dtype and shape of numpy arrays against the type annotation."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        match get_origin(source_type):
            case None:
                ndims = None
                item_type = None
            case np.ndarray:
                shape_type, item_type = get_args(source_type)
                item_type = get_args(item_type)[0]
                ndims = len(get_args(shape_type))
            case _:
                raise TypeError(f"unsupported type {source_type}")

        schema = handler(source_type)

        def check_array(a: np.ndarray):
            if ndims is not None and a.ndim != ndims:
                raise ValueError(f"the array must be {ndims}-dimensional")

            if item_type is not None and not np.issubdtype(a.dtype, item_type):
                a = np.asarray(a, dtype=item_type)

            return a

        return core_schema.no_info_after_validator_function(check_array, schema)


def serialize_array(a: np.ndarray):
    """Simple array serializer using `.tolist()`."""
    return a.tolist()


type NumpyArray1D[PyT, NpT: np.generic] = Annotated[
    np.ndarray[tuple[int], np.dtype[NpT]],
    ValidateAs(list[PyT], np.asarray),
    ArrayValidator,
    PlainSerializer(serialize_array),
]
"""Type annotation for pydantic fields storing a 1D numpy array with plain python type `PyT` and corresponding numpy type `NpT`. The field is validated and serialized as a `list[PyT]`."""

type NumpyArray2D[PyT, NpT: np.generic] = Annotated[
    np.ndarray[tuple[int, int], np.dtype[NpT]],
    ValidateAs(list[list[PyT]], np.asarray),
    ArrayValidator,
    PlainSerializer(serialize_array),
]
"""Type annotation for pydantic fields storing a 2D numpy array with plain python type `PyT` and corresponding numpy type `NpT`. The field is validated and serialized as a `list[list[PyT]]`."""
