#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Time    :   2021/09/11 15:17:44
@Contact :   noaghzil@gmail.com
@Desc    :   "some explore of metaclass features"
'''

# here put the import lib

import inspect

## === tool

def print_current_log(*arg):
    print(f"{arg} in Super {inspect.stack()[1][3]}")

class RunFeature(object):

    def run(self):
        print("Run Feature")

class FlyFeature(object):

    def fly(self):
        print("Fly Feature")


class EndueFeature(type):
    def __init__(obj, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def __new__(meta, name, base, attrs):
        futures_list = [RunFeature, FlyFeature]
        for one in futures_list:
            for name, func in inspect.getmembers(one, inspect.isfunction or inspect.ismethod):
                if name in attrs:
                    continue
                attrs[name] = func 
        obj = type.__new__(meta, name, base, attrs)
        # import pdb;pdb.set_trace()
        return obj

class Super(object, metaclass=EndueFeature):

    # def __str__(self) -> str:
    #     # import pdb;pdb.set_trace()
    #     return "%s.%s" % (__name__,self.__class__.__name__)

    def __new__(cls, *list, **map):
        print_current_log(cls)
        obj = super().__new__(cls)
        print_current_log(obj)
        return obj

    def __init__(self, *args, **kwargs):
        print_current_log(self)
        self.__name__ = "%s.%s" % (__name__,self.__class__.__name__)
        return super().__init__(*args, **kwargs)

    def __call__(self):
        # import pdb;pdb.set_trace()
        print_current_log(self.__name__, "test")


# hasattr()函数
## 该函数的功能是查找类的实例对象中是否包含指定名称的属性或者方法，
## 但该函数有一个缺陷，即它无法判断该指定的名称，到底是类属性还是类方法
# 解决方案:  借助可调用对象的概念：
## 类实例对象包含的方法，其实也属于可调用对象，但类属性却不是
if __name__ == "__main__":
    last  = Super()
    last()

