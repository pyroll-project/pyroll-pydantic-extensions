from typing import Annotated

import numpy as np
import pytest
from pydantic import ValidationError

from pyroll_pydantic_extensions import RegularGrid
from pyroll_pydantic_extensions.base_model import PyRollBaseModel
from pyroll_pydantic_extensions.static_field import ValidateGridShape


def test_base_model_annotations():
    class Model(PyRollBaseModel):
        num_field: int
        grid_field: RegularGrid[float, np.float64]
        mixed_grid_field: float | RegularGrid[float, np.float64]
        annotated_grid_field: Annotated[RegularGrid[float, np.float64], ValidateGridShape]

    Model(num_field=42, grid_field=[42, 21], mixed_grid_field=[[42, 21], [21, 42]], annotated_grid_field=[42, 21])


@pytest.mark.parametrize(
    ("field1", "field2", "allowed"),
    [
        ([42, 21], [[42, 21], [21, 42]], True),
        ([[42, 21]], [[42, 21], [21, 42]], True),
        ([42, 21, 1], [[42, 21], [21, 42]], False),
        # lower dimensional array is compared from the right!
        ([42, 21], [[42, 21], [21, 42], [1, 2]], True),
        ([42, 21, 2], [[42, 21], [21, 42], [1, 2]], False),
        ([[42, 21], [21, 42], [1, 2]], [42, 21], True),
        ([[42, 21], [21, 42], [1, 2]], [42, 21, 2], False),
    ],
)
def test_base_model_shape(field1, field2, allowed):
    class Model(PyRollBaseModel):
        field1: RegularGrid[float, np.float64]
        field2: RegularGrid[float, np.float64]

    if allowed:
        Model(field1=field1, field2=field2)
    else:
        with pytest.raises(ValidationError):
            m = Model(field1=field1, field2=field2)
            print(m.field1.shape, "×", m.field2.shape, "→", (m.field1 * m.field2).shape, ":\n", m.field1 * m.field2)
