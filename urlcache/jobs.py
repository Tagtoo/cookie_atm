from rq.decorators import job
import redis
from urllib2 import URLError


redis_conn = redis.Redis()

@job('caching', connection = redis_conn)
def cache_url(host, urlpath, timeout):
    from core import RedisBank
    from core import UrlCacher
    from utils import urlfetch
    bank = RedisBank()
    urlcacher = UrlCacher(bank)
    
    try:
        urlcacher.update(host, urlpath, timeout=timeout, async=True)
    except URLError:
        print 'URLError'

