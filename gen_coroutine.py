# coding=UTF-8
from tornado.gen import coroutine, Return#, sleep
from tornado.ioloop import IOLoop
from time import sleep
import functools

def cat():
    pass

def subroutine(func):
    print(dir(func))
    
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return decorator

@coroutine
def routine_ur(url, wait):
    print(url, wait)
    yield sleep(wait)
    print('routine_ur {} took {}s to get!'.format(url, wait))


@coroutine
def routine_url_with_return(url, wait):
    print(url, wait)
    yield sleep(wait)
    print('routine_url_with_return {} took {}s to get!'.format(url, wait))
    raise Return((url, wait))

# 非生成器协程，不会为之生成单独的 Runner()
# coroutine 运行结束后，直接返回一个已经执行结束的 future
@coroutine
def routine_simple():
    print("it is simple routine")

@coroutine
def routine_simple_return():
    print("it is simple routine with return")
    raise Return("value from routine_simple_return")

@coroutine
def routine_main():
    yield routine_simple()

    yield [routine_ur("url0", 1), routine_ur("url3", 3)]

    ret = yield routine_simple_return()
    print(ret)

    ret = yield [routine_url_with_return("url1", 1), routine_url_with_return("url2", 2)]
    #print(ret)



if __name__ == '__main__':
    IOLoop.instance().run_sync(routine_main)


