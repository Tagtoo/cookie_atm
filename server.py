import tornado
import tornado.web
import tornado.gen
import tornadoredis
from tornado import httpclient

from urlcache.core import RedisBank, UrlCacher

from utils import Router
import logging

try:
    import atm_settings
except:
    raise('Please create atm_settings.py for configuration')

CONNECTION_POOL = tornadoredis.ConnectionPool(max_connections=atm_settings.REDIS_CONN_MAX, wait_for_available=True)

def send_message(url, body=None, callback=None):
    """
    if handler == None: send a sync request
    else handler == <function>: send async request
    """
    request = httpclient.HTTPRequest(url)

    if body:
        request.body = body
        request.method = 'POST'
    else:
        request.method = 'GET'

    client = httpclient.HTTPClient()
    response = client.fetch(request)
    print "HTTPRequest:%s:%s" % (url, len(response.body))
    return response.body

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

    def init_timeouts(self):
        self.timeout_rules = self.atm_settings.SPECIAL_TIMEOUTS
        
    def initialize(self):
        self.router = Router()
        self.redis_bank = RedisBank()
        self.url_cacher = UrlCacher(self.redis_bank)
        self.atm_settings = atm_settings
        self.timeout_rules = {}

        self.init_routes()
        self.init_timeouts()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        c = tornadoredis.Client(connection_pool=CONNECTION_POOL)
        request = self.request
        url_path = request.path

        logger = logging.getLogger('tornado.application')
        logger.info(url_path)

        if self.router.exist_route(url_path):
            # determine timeout
            if url_path in self.timeout_rules:
                timeout = self.timeout_rules[url_path]
            else:
                timeout = self.atm_settings.DEFAULT_TIMEOUT

            query = request.query
            host = self.router.get_route(url_path)
            logger.info(host)

            query_url_path = "%s?%s" % (url_path, query) if query else url_path
            logger.info("Request: %s" % query_url_path)

            exists = yield tornado.gen.Task(c.exists, query_url_path)
            
            if exists:
                print 'exists'
                response = yield tornado.gen.Task(c.get, query_url_path)
                yield tornado.gen.Task(c.disconnect)
                self.write(response)
                self.finish()
            else:
                print 'not exsits'
                content_url = "%s%s" % (host, query_url_path)
                content_to_cache = send_message(content_url)

                #cache_result = yield tornado.gen.Task(c.setex, query_url_path, content_to_cache, 3600)
                print query_url_path, len(content_to_cache)
                cache_result = yield tornado.gen.Task(c.setex, query_url_path, 3600, content_to_cache)
                yield tornado.gen.Task(c.disconnect)
                self.write('')
                self.finish()


    @tornado.web.asynchronous
    def post(self):
        request = self.request
        url_path = request.path

        if self.router.exist_route(url_path):
            host = self.router.get_route(url_path)
            print host, url_path
            if self.request.body:
                print 'body: %s' % self.request.body
                content = self.request.body
                self.write(self.url_cacher.update(host, url_path, content))
            else:
                self.write(self.url_cacher.update(host, url_path))

        self.finish()
        

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/.*", UrlCacheHandler),
    ])
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
