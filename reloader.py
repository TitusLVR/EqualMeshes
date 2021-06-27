#Util imports
import sys
import importlib
from pkgutil import iter_modules
from pathlib import Path
from inspect import isclass, ismodule

#Project imports
from em import root_module_name

#This is useful for module reloading when using the 'Reload Scripts' option inside Blender
#It is not pretty, and I'm not sure if there's a much better way to handle it completely automatically
def reload_all_modules():
    root_dir = Path(__file__).parent
    modulenames = []
    _list_modules(modulenames, root_dir, root_module_name)
    _reload_all_modules(modulenames, root_dir, root_module_name)

def _reload_all_modules(modulenames, path, module_path):
    if module_path:
        module_path += '.'

    for (_, modulename, ispkg) in iter_modules([path]):
        if ispkg:
            _reload_all_modules(modulenames, path.joinpath(modulename), module_path + modulename)
        elif module_path + modulename in sys.modules:
            module = sys.modules[module_path + modulename]
            
            for vn in dir(module):
                v = getattr(module, vn)
                if not ismodule(v):
                    continue
                v_name = v.__name__
                if v_name in modulenames and v_name in sys.modules:
                    importlib.reload(sys.modules[v_name])
            importlib.reload(module)

def _list_modules(modulenames, path, module_path):
    if module_path:
        module_path += '.'

    for (_, modulename, ispkg) in iter_modules([path]):
        if ispkg:
            modulenames.append(module_path + modulename)
            _list_modules(modulenames, path.joinpath(modulename), module_path + modulename)
        else:
            modulenames.append(module_path + modulename)