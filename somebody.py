# -*- coding: utf-8 -*-

class People(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def Hello(self):
        print("我叫%s，今年%s岁"%(self.name, self.age))