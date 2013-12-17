import tornado
import tornado.web

from urlcache.core import RedisBank, UrlCacher

from utils import Router
import logging

try:
    import atm_settings
except:
    raise('Please create atm_settings.py for configuration')


class UrlCacheHandler(tornado.web.RequestHandler):
    """
    Default handler
    """
    def init_routes(self):
        """
        Putting routes into router
        """
        # deal with default rules
        default_target = self.atm_settings.DEFAULT_PROXIED_HOST
        
        for url in self.atm_settings.PROXIED_URLS:
            self.router.add_route(url, default_target)
        
        # deal with special rules
        for path, host in self.atm_settings.SPECIAL_ROUTES.items():
            self.router.add_route(path, host)
        
    def initialize(self):
        self.router = Router()
        self.redis_bank = RedisBank()
        self.url_cacher = UrlCacher(self.redis_bank)
        self.atm_settings = atm_settings

        self.init_routes()

    def get(self):
        request = self.request
        url_path = request.path

        logger = logging.getLogger('tornado.application')
        logger.info(url_path)

        if self.router.exist_route(url_path):
            query = request.query
            host = self.router.get_route(url_path)
            logger.info(host)

            query_url_path = "%s?%s" % (url_path, query)
            print "Request: %s" % query_url_path
            response = self.url_cacher.query(host, query_url_path)
            self.write(response)

    def post(self):
        request = self.request
        url_path = request.path

        if self.router.exist_route(url_path):
            host = self.router.get_route(url_path)
            print host, url_path
            if self.request.body:
                content = self.request.body
                self.write(self.url_cacher.update(host, url_path, content))
            else:
                self.write(self.url_cacher.update(host, url_path))
        

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/.*", UrlCacheHandler),
    ])
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
