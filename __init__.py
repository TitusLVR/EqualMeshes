bl_info = {
    'name': 'Equal Meshes',
    'author': 'Nacho Sanchez',
    'version': (0, 1, 0, 0),
    'blender': (2, 80, 0),
    'category': 'Mesh'
}

#Util imports
import sys

#Alias for 'equalmeshes' or whatever the name of the root folder
root_module_name = 'em'
sys.modules[root_module_name] = sys.modules[__name__]

#Blender imports
import bpy

#Project imports
from em.reloader import reload_all_modules
from em.registrator import register_all_classes, unregister_all_classes

def register():
    reload_all_modules()
    register_all_classes()

def unregister():
    unregister_all_classes()

if __name__ == '__main__':
    register()