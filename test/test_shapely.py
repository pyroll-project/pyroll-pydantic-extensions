from pathlib import Path

import pytest
import shapely
from pydantic import BaseModel, TypeAdapter, ValidationError

from pyroll_pydantic_extensions.shapely import LineString, Polygon

ta = TypeAdapter(Polygon)


@pytest.mark.parametrize(
    "value",
    [
        "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
        [(0, 0), (0, 1), (1, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)],
        shapely.Polygon([(0, 0), (0, 1), (1, 1), (1, 0)]),
        shapely.Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]),
    ],
)
def test_correct_values(value, tmpdir: Path):
    v = ta.validate_python(value)

    result = ta.dump_json(v).decode("utf8")
    assert result == '"POLYGON ((0 0, 0 1, 1 1, 1 0, 0 0))"'
    (tmpdir / "result.txt").write_text(result, encoding="utf8")


@pytest.mark.parametrize(
    "value",
    [
        [(0, 0), (0, "a"), (1, 1), (1, 0)],
        [[(0, 0), (0, 1), (1, 1), (1)]],
        [[(0, 0), (0, 1), (1, 0), (1, 1), (0, 0)]],
    ],
)
def test_errors(value, tmpdir: Path):
    with pytest.raises(ValidationError) as info:
        ta.validate_python(value)

    (tmpdir / "exception.txt").write_text(str(info.getrepr()), encoding="utf8")


def test_model():

    class Model(BaseModel):
        poly_field: Polygon
        line_field: LineString

    Model(
        poly_field=shapely.Point([0, 0]).buffer(1),
        line_field=shapely.LineString([[0, 0], [1, 1]]),
    )
