# -*- coding: UTF-8 -*-
from __future__ import absolute_import
import opentracing
import logging
import importlib, inspect, functools
import imp, six, sys, re

DEFAULT_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
DEFAULT_LEVEL = logging.INFO

def get_trace_log(name='trace_log', level=DEFAULT_LEVEL, fmt=DEFAULT_FORMAT):
    trace_log = logging.getLogger(name)
    trace_log.setLevel(level)
    formatter = logging.Formatter(fmt)
    logHandler = logging.StreamHandler()
    logHandler.setFormatter(formatter)
    trace_log.addHandler(logHandler)
    return trace_log

class MetaPathFinder:
    def __init__(self, patch, log_level=DEFAULT_LEVEL):
        self.patch = patch
        self.log = get_trace_log('meta_path_finder', log_level)

    def find_module(self, fullname, path=None):
        filter_module = ['opentracing_instrumentation', 'opentracing', 'future', 'kfztoolbox']
        for module in filter_module:
            if module in fullname:
                return None
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
        self.log.debug("[PATCH] find_module: %s" % fullname)
        return MetaPathLoader(self.patch)


class MetaPathLoader:
    def __init__(self, patch, log_level=DEFAULT_LEVEL):
        self.patch = patch
        self.log = get_trace_log('meta_path_loader', log_level)

    def load_module(self, fullname, path=None):
        self.log.debug("[PATCH] load_module: %s" % fullname)
        if fullname in sys.modules:
            return sys.modules[fullname]
        # 先从 sys.meta_path 中删除自定义的 finder
        # 防止下面执行 import_module 的时候再次触发此 finder
        # 从而出现递归调用的问题
        finder = sys.meta_path.pop(0)
        try:
            module = importlib.import_module(fullname)
        except Exception as e:
            self.log.warning("[PATCH] except_module: %s error %s" % (fullname, e))
            if six.PY3:
                fullname_arr = fullname.split('.')
                name = fullname_arr.pop()
                path = fullname_arr.pop()
                module = importlib.import_module(name, path)
                return module
            else:
                return None
        module = self.patch.traced_module(module)
        sys.meta_path.insert(0, finder)
        #print("meta_path:", sys.meta_path)
        return module

def install_patch(patch, debug=False):
    """
    Install patche to decorate modules During import
    """
    log_level = logging.DEBUG if debug else logging.ERROR

    sys.meta_path.insert(0, MetaPathFinder(patch, log_level))