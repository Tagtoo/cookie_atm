import tornado
from urlcache.core import RedisBank

class UrlCacheHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.redis_bank = RedisBank()
    def get(self):
        pass
        
        

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/.*", UrlCacheHandler),
    ])
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
