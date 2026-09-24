import numpy as np

from pyroll_pydantic_extensions.numpy import RegularGrid

type StaticField[PyT, NpT: np.generic] = PyT | RegularGrid[PyT, NpT]
