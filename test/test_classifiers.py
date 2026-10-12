from pathlib import Path

import pytest
from pydantic import BaseModel, TypeAdapter, ValidationError

from pyroll_pydantic_extensions.classifiers import Classifiers

ta = TypeAdapter(Classifiers)


@pytest.mark.parametrize(
    "value",
    [
        "abc",
        ["abc"],
        ["abc", "def"],
        {"abc", "def"},
    ],
)
def test_correct_values(value, tmpdir: Path):
    v = ta.validate_python(value)

    (tmpdir / "result.txt").write_text(ta.dump_json(v).decode("utf8"), encoding="utf8")


@pytest.mark.parametrize(
    "value",
    [
        3,
        set(),
        [],
        [3],
        {3},
    ],
)
def test_errors(value, tmpdir: Path):
    with pytest.raises(ValidationError) as info:
        ta.validate_python(value)

    (tmpdir / "exception.txt").write_text(str(info.getrepr()), encoding="utf8")


def test_model():

    class Model(BaseModel):
        field: Classifiers

    Model(field=["abc"])
    Model(field="abc")
    Model(field={"abc"})
