# coding=UTF-8
# email：noaghzil@gmail.com
import time
import logging
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

tornado.options.parse_command_line()

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write("Hello, world")
        self.finish()

class ActionHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(4)
    
    @gen.coroutine
    def post(self):
        action = self.get_argument('action', '')
        print("Noagh")
        if hasattr(self, action):
            yield self.action_executor(action)
        else:
            self.write(dict(status=1, message='没有找到对应的action'))
            return
    
    @run_on_executor
    def action_executor(self, action):
        action_handle = getattr(self, action) 
        action_handle("url1", 10)
    
    def sleep(self, url, wait):
        print(url, wait)
        time.sleep(wait)
        print('routine_url_with_return {} took {}s to get!'.format(url, wait))

        

# 基于 Tornado 协议的异步库，非阻塞
class NoBlockingHnadler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        # 协程来回切换执行 
        # 非阻塞耗时：max(url1, url2)
        start_time =time.time()
        yield [self.routine_url_with_return("url1", 3), self.routine_url_with_return("url2", 7)]
        self.write('Blocking Request')
        print(time.time()-start_time)

    @gen.coroutine
    def routine_url_with_return(self, url, wait):
        print(url, wait)
        yield gen.sleep(wait)
        print('routine_url_with_return {} took {}s to get!'.format(url, wait))   
    

 # 基于ThreadPoolExecutor线程的异步编程，非阻塞
 # 缺点：大量使用线程化的异步函数做一些高负载的活动，会导致该 Tornado 进程性能低下响应缓慢
 # ThreadPoolExecutor 是对标准库中的 threading 的高度封装，
 # 利用线程的方式让阻塞函数异步化，解决了很多库是不支持异步的问题。
class NoBlockingHnadler2(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    def get(self):
        start_time =time.time()
        # 协程来回切换执行 
        # 阻塞耗时：sum(url1, url2)
        yield [self.routine_url_with_return("url1", 3), self.routine_url_with_return("url3", 7)]
        #print(yield self.routine_url_with_return("url3", 7))
        #yield [self.routine_url_with_return("url1", 3), self.routine_url_with_return("url3", 7)]
        self.write('Blocking Request')
        print(time.time()-start_time)
    
    @run_on_executor
    def routine_url_with_return(self, url, wait):
        print(url, wait)
        time.sleep(wait)
        print('routine_url_with_return {} took {}s to get!'.format(url, wait))
        return "routine_url_with_return %s"%wait



# 阻塞其他的请求, 非基于 Tornado 协议的异步库
class BlockingHnadler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    def get(self):
        start_time =time.time()
        # 协程来回切换执行 
        # 阻塞耗时：sum(url1, url2)
        yield [self.routine_url_with_return("url1", 3), self.routine_url_with_return("url3", 7)]
        self.write('Blocking Request')
        print(time.time()-start_time)
    
    @gen.coroutine
    def routine_url_with_return(self, url, wait):
        print(url, wait)
        yield time.sleep(wait)
        print('routine_url_with_return {} took {}s to get!'.format(url, wait))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/block", BlockingHnadler),
        (r"/noblock", NoBlockingHnadler),
        (r"/noblock2", NoBlockingHnadler2),
        (r"/action", ActionHandler),
    ], autoreload=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()