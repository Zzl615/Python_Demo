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


class Hook:
    def hack(self, module):
        return module


class Loader:
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
        # TODO: 1. importlib和imp切换
        # 2. sys.path_hook和sys.meta_path和sys.modules
        # url: https://testerhome.com/articles/19261
        self.module = importlib.import_module(name)
        sys.meta_path.insert(0, self)
        return self

    def load_module(self, name):
        '''
           py2和py3.4之前的加载器
        '''
        if not self.module:
            raise ImportError("Unable to load module.")
        module = self.module
        for hacker in _hackers:
            module = hacker.hack(module)
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
