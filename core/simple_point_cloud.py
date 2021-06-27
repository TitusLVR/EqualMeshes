#Util imports
import numpy as np

#Blender imports
import mathutils

#Project imports
from em.core.utils import conversions as conv

class SimplePointCloud:
    def __init__(self, obj):
        self.wm = np.array(obj.matrix_world)

        #These are the absolute positions of the mesh's vertices (as you see them in the viewport), so,
        #with object transforms 'applied'
        self.abs_points = self.wm.dot(np.array([conv.Vector3D_4D(v.co) for v in obj.data.vertices]).T).T