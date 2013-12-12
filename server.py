import tornado
import tornado.web
from urlcache.core import RedisBank, UrlCacher

import atm_settings

try:
    import atm_settings
except:
    pass


class UrlCacheHandler(tornado.web.RequestHandler):
    def get_proxied_uris(self):
        return atm_settings.PROXIED_URIS

    def initialize(self):
        self.redis_bank = RedisBank()
        self.url_cacher = UrlCacher(atm_setting.PROXIED_TARGET, self.redis_bank)

    def get(self):
        request = self.request
        url_path = request.path

        if url_path in self.get_proxied_uris():
            url_path = request.path
            self.write(self.url_cacher.query(url_path))

    def post(self):
        request = self.request
        url_path = request.path


        if url_path in self.get_proxied_uris():
            if self.request.body:
                content = self.request.body
                self.write(self.url_cacher.update(url_path, content))
            else:
                self.write(self.url_cacher.update(url_path))
        

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/.*", UrlCacheHandler),
    ])
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
