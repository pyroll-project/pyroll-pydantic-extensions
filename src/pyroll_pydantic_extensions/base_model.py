import numpy as np
from pydantic import BaseModel, model_validator
from typing_inspection.introspection import AnnotationSource, inspect_annotation

from pyroll_pydantic_extensions.static_field import ValidateGridShape


class PyRollBaseModel(BaseModel):
    @model_validator(mode="after")
    def validate_regular_grids_shape(self):
        cls = type(self)

        shape: tuple | None = None

        for key, info in cls.model_fields.items():
            insp_ann = inspect_annotation(
                info.annotation, annotation_source=AnnotationSource.CLASS, unpack_type_aliases="eager"
            )
            resolved_metadata = set(info.metadata + insp_ann.metadata)

            if ValidateGridShape in resolved_metadata:
                value = getattr(self, key)

                if isinstance(value, np.ndarray):
                    if not shape:
                        shape = value.shape
                    else:
                        np.broadcast_shapes(shape, value.shape)

        return self
