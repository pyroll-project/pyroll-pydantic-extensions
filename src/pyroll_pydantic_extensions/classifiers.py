from typing import Annotated

from pydantic import BeforeValidator, Field

type Classifiers = Annotated[
    set[str],
    Field(min_length=1),
    BeforeValidator(lambda v: {v} if isinstance(v, str) else v),
]
