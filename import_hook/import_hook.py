# -*- coding: utf-8 -*-

import sys
import six
import imp
import os
import importlib
import traceback

_hackers = []


def register(obj):
    _hackers.append(obj)


class Hook(object):
    def hack(self, module):
        return module


class Loader(object):
    '''
       import导入器实现，兼容py2和py3
    '''

    def __init__(self):
        self.module = None

    def find_module(self, name, path):
        '''
           py2和py3.4之前的查找器
        '''      
        sys.meta_path.remove(self)
        name_array = name.split('.')
        name = name_array.pop()
        self.module_finder, self.path_name, self.sedescription = imp.find_module(name, path)
        if self.module_finder is None:
            sys.meta_path.insert(0, self)
            return None
        return self

    def load_module(self, name):
        '''
           py2和py3.4之前的加载器
        '''     
        try:
            module_finder = imp.load_module(name, self.module_finder, self.path_name, self.sedescription)
        except Exception as e:
            sys.meta_path.insert(0, self)
            print("except_load_module: %s Exception %s traceback: %s" % (name, e, traceback.print_exc()))
        else:
            sys.meta_path.insert(0, self)
            for hacker in _hackers:
                module = hacker.hack(module_finder)
            return module

    def find_spec(self, fullname, path, target=None):
        '''
           py3.4之后的查找器
        '''
        try:
            sys.meta_path.remove(self)
            module_spec = importlib.util.find_spec(fullname)
            module_spec.loader = self
        except Exception as e:
            print("except_find_spec: %s Exception %s traceback: %s" % (fullname, e, traceback.print_exc()))
            sys.meta_path.insert(0, self)
            return None
        else:
            return module_spec

    def create_module(self, spec):
        '''
           py3.4之后的创造器，用于创建模块
        '''
        try:
            module = importlib.import_module(spec.name)
        except Exception as e:
            print("except_find_spec: %s Exception %s traceback: %s" % (fullname, e, traceback.print_exc()))
            sys.meta_path.insert(0, self)
            return None
        else:
            sys.meta_path.insert(0, self)
            return module

    def exec_module(self, module):
        '''
           py3.4之后的执行器，用于创建模块，每次执行引入模块或者重载模块时会执行的操作
        '''
        for hacker in _hackers:
            module = hacker.hack(module)
        return module


sys.meta_path.insert(0, Loader())
