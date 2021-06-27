#Util imports
import numpy as np

def Vector3D_4D(v):
    return np.array([v[0], v[1], v[2], 1.])

def Vector4D_3D(v):
    return np.array([v[0], v[1], v[2]])

def Matrix_3D_4D(m):
    return np.array([
        [m[0][0], m[0][1], m[0][2], 0],
        [m[1][0], m[1][1], m[1][2], 0],
        [m[2][0], m[2][1], m[2][2], 0],
        [0      , 0      , 0      , 1]
    ])
