from pathlib import Path

import numpy as np
import pytest
from pydantic import BaseModel, TypeAdapter, ValidationError

from pyroll_pydantic_extensions.static_field import StaticField

ta = TypeAdapter(StaticField[float, np.float64])


@pytest.mark.parametrize(
    "value",
    [
        3,
        "3",
        [2, 4],
        [2, "4"],
        [[3, 5], [1, 3]],
        [[3, "5"], [1, 3]],
        np.array([[3, 5], [1, 3]]),
        np.array([[3, "5"], [1, 3]]),
    ],
)
def test_correct_values(value, tmpdir: Path):
    v = ta.validate_python(value)

    (tmpdir / "result.txt").write_text(ta.dump_json(v).decode("utf8"), encoding="utf8")


@pytest.mark.parametrize(
    "value",
    [
        None,
        [[2], 4],
        ["a", 4],
        [[[3, 5], [1, 3]]],
        np.array([[3, 5], [1, "a"]]),
    ],
)
def test_errors(value, tmpdir: Path):
    with pytest.raises(ValidationError) as info:
        ta.validate_python(value)

    (tmpdir / "exception.txt").write_text(str(info.getrepr()), encoding="utf8")


def test_model():

    class Model(BaseModel):
        grid_field: StaticField[float, np.float64]

    Model(grid_field=[3, 5])
    Model(grid_field=[[3, 5], [1, 3]])
    Model(grid_field=np.array([[3, 5], [1, 3]]))
