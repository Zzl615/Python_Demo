class CLanguage:
    a = 1
    b = 2
    def __init__ (self):
        self.name = "C语言中文网"
        self.add = "http://c.biancheng.net"
    def get(self):
        pass
       
class CL(CLanguage):
    c = 1
    d = 2
    def __init__ (self):
        self.na = "Python教程"
        self.ad = "http://c.biancheng.net/python"
#父类名调用__dict__
print(CLanguage.__dict__)
#子类名调用__dict__
print(CL.__dict__)
#父类实例对象调用 __dict__
# clangs = CLanguage()
# print(clangs.__dict__)
# #子类实例对象调用 __dict__
# cl = CL()
# print(cl.__dict__)