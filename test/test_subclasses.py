from pathlib import Path
from typing import Annotated, Literal

import pytest
from pydantic import BaseModel, ValidationError

from pyroll_pydantic_extensions.subclass import ValidateSubclasses


class Base(BaseModel):
    type: Literal["base"] = "base"


class Sub1(Base):
    type: Literal["sub1"] = "sub1"
    val: int


class Sub2(Base):
    type: Literal["sub2"] = "sub2"
    val: str


@pytest.mark.parametrize(
    ("value", "subclass"),
    [
        ({"subclassed": {"type": "base"}}, Base),
        ({"subclassed": {"type": "sub1", "val": "42"}}, Sub1),
        ({"subclassed": {"type": "sub2", "val": "42"}}, Sub2),
    ],
)
def test_with_base(value, subclass, tmpdir: Path):

    class Container(BaseModel):
        subclassed: Annotated[Base, ValidateSubclasses(Base, True)]

    v = Container.model_validate(value)

    result = v.model_dump_json()
    (tmpdir / "result.txt").write_text(result, encoding="utf8")

    assert isinstance(v.subclassed, subclass)


def test_without_base(tmpdir: Path):

    class Container(BaseModel):
        subclassed: Annotated[Base, ValidateSubclasses(Base, False)]

    v = Container.model_validate({"subclassed": {"type": "sub1", "val": "42"}})

    result = v.model_dump_json()
    (tmpdir / "result_sub.txt").write_text(result, encoding="utf8")

    assert isinstance(v.subclassed, Sub1)

    with pytest.raises(ValidationError):
        Container.model_validate({"subclassed": {"type": "base"}})


def test_new_subclass(tmpdir: Path):

    class Container(BaseModel):
        subclassed: Annotated[Base, ValidateSubclasses(Base)]

    # new subclass after Container has been defined
    class Sub3(Base):
        type: Literal["sub3"] = "sub3"
        val: int

    # Sub1 must still work
    v = Container.model_validate({"subclassed": {"type": "sub1", "val": "42"}})
    result = v.model_dump_json()
    (tmpdir / "result_sub1.txt").write_text(result, encoding="utf8")
    assert isinstance(v.subclassed, Sub1)

    # Sub3 is not known, as it did not exist as schema was build
    with pytest.raises(ValidationError):
        Container.model_validate({"subclassed": {"type": "sub3", "val": "42"}})

    # force model rebuild
    Container.model_rebuild(force=True)

    # now Sub3 must work
    v = Container.model_validate({"subclassed": {"type": "sub3", "val": "42"}})
    result = v.model_dump_json()
    (tmpdir / "result_sub3.txt").write_text(result, encoding="utf8")
    assert isinstance(v.subclassed, Sub3)
