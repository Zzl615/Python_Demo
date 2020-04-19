"""modulehacker module"""


import sys, six,imp
import importlib

_hackers = []


def register(obj):
    _hackers.append(obj)


class Hook:
    def hack(self, module):
        return module

class MetaPathFinder:
    def __init__(self):
        pass

    def find_module(self, fullname, path=None):
        finder = sys.meta_path.pop(0)
        if not six.PY34:
            fullname_arr = fullname.split('.')
            name = fullname_arr.pop()
            module_info, path_name, description = imp.find_module(name, path)
            sys.meta_path.insert(0, finder)
            if module_info is None:
                return None
        else:
            module_spec = importlib.util.find_spec(fullname)
            sys.meta_path.insert(0, finder)
            if module_spec is None:
                return None
        return MetaPathLoader()


class MetaPathLoader:
    def __init__(self):
        pass

    def load_module(self, fullname, path=None):
        if fullname in sys.modules:
            return sys.modules[fullname]
        finder = sys.meta_path.pop(0)
        module = importlib.import_module(fullname)
        for hacker in _hackers:
            module = hacker.hack(module)
        sys.meta_path.insert(0, finder)
        #print("meta_path:", sys.meta_path)
        return module

class Loader:
    def __init__(self):
        self.module = None

    def find_module(self, name, path):
        sys.meta_path.remove(self)
        self.module = importlib.import_module(name)
        sys.meta_path.insert(0, self)
        return self.load_module(name)

    def load_module(self, name):
        if not self.module:
            raise ImportError("Unable to load module.")
        module = self.module
        finder = sys.meta_path.pop(0)
        for hacker in _hackers:
            module = hacker.hack(module)
            # print(module)
            # print(module.__doc__)
        sys.meta_path.insert(0, finder)
        return module

sys.meta_path.insert(0, MetaPathFinder())
