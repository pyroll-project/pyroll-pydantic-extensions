from typing import Annotated

import numpy as np
from typing_extensions import sentinel

from pyroll_pydantic_extensions.numpy import NumpyArray1D, NumpyArray2D

ValidateGridShape = sentinel("ValidateGridShape")

type RegularGrid[PyT, NpT: np.generic] = Annotated[NumpyArray1D[PyT, NpT] | NumpyArray2D[PyT, NpT], ValidateGridShape]
type StaticField[PyT, NpT: np.generic] = PyT | RegularGrid[PyT, NpT]
