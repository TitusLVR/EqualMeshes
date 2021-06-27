#Util imports
import random
import math
import numpy as np

#Blender imports
import mathutils

#Project imports
from em.core.utils import conversions as conv
from em.core.simple_point_cloud import SimplePointCloud

class SimpleSolver:
    def __init__(self, obj_from, obj_to):
        self.cloud_from = SimplePointCloud(obj_from)
        self.cloud_to = SimplePointCloud(obj_to)

    def Solve(self):
        #We gather three random samples from each cloud
        idxs = random.sample(range(len(self.cloud_from.abs_points)), 3)

        f_1 = self.cloud_from.abs_points[idxs[0]][:3]
        f_2 = self.cloud_from.abs_points[idxs[1]][:3]
        f_3 = self.cloud_from.abs_points[idxs[2]][:3]

        t_1 = self.cloud_to.abs_points[idxs[0]][:3]
        t_2 = self.cloud_to.abs_points[idxs[1]][:3]
        t_3 = self.cloud_to.abs_points[idxs[2]][:3]

        #We now build two local coordinate systems, one for each simple cloud
        #===Coordinate systems===
        x_f = f_2 - f_1
        x_t = t_2 - t_1

        #We calculate scale in the middle of this process
        #Since we know vertex order matches,
        scale = np.linalg.norm(x_t) / np.linalg.norm(x_f)

        x_f /= np.linalg.norm(x_f)
        x_t /= np.linalg.norm(x_t)
        
        y_f = f_3 - f_1 - (f_3 - f_1).dot(x_f) * x_f
        y_f /= np.linalg.norm(y_f)
        z_f = np.cross(x_f, y_f)

        y_t = t_3 - t_1 - (t_3 - t_1).dot(x_t) * x_t
        y_t /= np.linalg.norm(y_t)
        z_t = np.cross(x_t, y_t)

        #========================

        m_f = np.vstack([x_f, y_f, z_f])
        m_t = np.vstack([x_t, y_t, z_t]).T

        #This is the rotation we are looking for
        rotation = m_t.dot(m_f)

        #Now, the translation can be simply written as
        t_vec = t_1 - scale * rotation.dot(f_1)
        translation = np.array(mathutils.Matrix.Translation(conv.Vector3D_4D(t_vec)))

        transform = translation.dot(mathutils.Matrix(conv.Matrix_3D_4D(scale * rotation)))

        #These are the transformed absolute points of the 'from mesh' based on 'transform'
        transformed = transform.dot(self.cloud_from.abs_points.T).T

        #Maximum of distances after aligning
        max_distance = np.max(np.linalg.norm(transformed - self.cloud_to.abs_points, axis=1))

        return max_distance