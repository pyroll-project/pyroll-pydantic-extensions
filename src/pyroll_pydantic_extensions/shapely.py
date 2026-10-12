from typing import Annotated

import shapely
from pydantic_shapely import GeometryField

type Polygon = Annotated[
    shapely.Polygon,
    GeometryField(z_values="forbid"),  # type: ignore
]
"""Type annotation for pydantic fields storing a shapely polygon."""

type LineString = Annotated[
    shapely.LineString,
    GeometryField(z_values="forbid"),  # type: ignore
]
"""Type annotation for pydantic fields storing a shapely line string."""
