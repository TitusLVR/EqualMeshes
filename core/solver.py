#Util imports
import numpy as np

#Blender imports
import bpy
import mathutils

#Project imports
from em.core.utils import conversions as conv
from em.core.point_cloud import PointCloud

#Main solver for rigid transforms
#NumPy's utilities and data structures are preferred. However, there are some functions from
#Mathutils that prove to be useful, mainly conversions.
#There is still much room for perfomance improvements
class Solver:
    def __init__(self, obj_from, obj_to):
        #PointCloud representations of the objects to be compared
        self.cloud_from = PointCloud(obj_from)
        self.cloud_to = PointCloud(obj_to)

    def solve(self):
        scale = self.solve_scale()
        rotation = self.solve_rotation()
        translation = self.solve_translation(scale, rotation)

        #The proposed rigid transform
        transform = translation.dot(scale * rotation)
        
        #These are the transformed absolute points of the 'from mesh' based on 'transform'
        transformed = transform.dot(self.cloud_from.abs_points.T).T

        max_distance = np.max(np.linalg.norm(transformed - self.cloud_to.abs_points, axis=1))
        return mean_distance

    def solve_scale(self):
        num = np.sum(np.square(self.cloud_to.rel_points))
        den = np.sum(np.square(self.cloud_from.rel_points))
        return ((num / den) ** (1 / 2))

    def solve_rotation(self):
        #The rotation matrix
        matrix = np.zeros((4,4))

        #Matrix representations of both relative point clouds
        from_matrices = np.array([Solver.from_vert_to_matrix(v) for v in self.cloud_from.rel_points])
        to_matrices = np.array([Solver.to_vert_to_matrix(v) for v in self.cloud_to.rel_points])

        #This matrix's max eigenvalue is used to compute rotation
        matrix = np.sum(np.matmul(from_matrices, to_matrices), axis=0)
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        #Eigenvectors are returned by numpy as column vectors, so we transpose
        eigenvectors = np.transpose(eigenvectors)
        max_eigval_idx = np.argmax(eigenvalues)
        max_eigenvector = eigenvectors[max_eigval_idx]
        
        #A quaternion representation of our max eigenvector
        eig_qr = mathutils.Quaternion(max_eigenvector)
        return np.array(eig_qr.to_matrix().to_4x4())

    def solve_translation(self, scale, rotation):
        t_vector = self.cloud_to.centroid - scale * rotation.dot(self.cloud_from.centroid.T)
        return np.array(mathutils.Matrix.Translation(conv.Vector4D_3D(t_vector)))

    @staticmethod
    def from_vert_to_matrix(fv):
        fvm = np.array([
            [0     ,-fv[0] ,-fv[1] ,-fv[2]],
            [fv[0] ,0      ,fv[2]  ,-fv[1]],
            [fv[1] ,-fv[2] ,0      ,fv[0] ],
            [fv[2] ,fv[1]  ,-fv[0] ,0     ]
        ])
        return np.transpose(fvm)

    @staticmethod
    def to_vert_to_matrix(tv):
        tvm = np.array([
            [0     ,-tv[0] ,-tv[1] ,-tv[2]],
            [tv[0] ,0      ,-tv[2] ,tv[1] ],
            [tv[1] ,tv[2]  ,0      ,-tv[0]],
            [tv[2] ,-tv[1] ,tv[0]  ,0     ]
        ])
        return tvm
