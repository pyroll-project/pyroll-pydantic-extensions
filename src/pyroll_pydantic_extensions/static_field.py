from typing import Annotated

import numpy as np
from typing_extensions import sentinel

from pyroll_pydantic_extensions.numpy import NumpyArray1D, NumpyArray2D

ValidateGridShape = sentinel("ValidateGridShape")
"""Metadata annotation that tells a model validator in `PyRollBaseModel` to check if the shapes of the marked fiedls are compatible (boradcastable) to each other."""

type RegularGrid[PyT, NpT: np.generic] = Annotated[NumpyArray1D[PyT, NpT] | NumpyArray2D[PyT, NpT], ValidateGridShape]
"""Type annotation that allows either a 1D or 2D numpy array of the respective type."""

type StaticField[PyT, NpT: np.generic] = PyT | RegularGrid[PyT, NpT]
"""Type annotation that allows either a scalar, a 1D or 2D numpy array of the respective type."""
