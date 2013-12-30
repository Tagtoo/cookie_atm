import redis
import urllib2
from multiprocessing import Process
from utils import urlfetch
from jobs import cache_url


class RedisBank(object):
    def __init__(self, host='localhost'):
        self.pool = redis.ConnectionPool(host=host)
        self.redis_client = redis.Redis(connection_pool=self.pool)

    def set(self, key, value, blocking=True, expire_time=3600):
        """
        blocking: do threading (not finished)
        expire_time: (seconds) the expiration time for stored key
        """
        if blocking and expire_time:
            self.redis_client.setex(key, value, expire_time)
        elif blocking:
            self.redis_client.set(key, value)
        else:
            rt = RedisThreadSave(self.pool, key, value)
            rt.start()

    def get(self, key):
        return self.redis_client.get(key)

    def exists(self, key):
        return self.redis_client.exists(key)

    def delete(self, key):
        """
        delete key
        """
        return self.redis_client.delete([key])


class RedisThreadSave(object):
    @classmethod
    def set_to_redis(cls, redis_client, key, value):
        redis_client.set(key, value)

    def __init__(self, redis_pool, key, value):
        self.redis_client = redis.Redis(connection_pool=redis_pool)
        self.process = Process(target=RedisThreadSave.set_to_redis, args=(self.redis_client, key, value))

    def start(self):
        self.process.start()


class UrlCacher(object):
    def __init__(self, bank):
        self.bank = bank

    def get_query_url(self, host, urlpath):
        return "%s/%s" % (host, urlpath)

    def query(self, host, urlpath, timeout=10, callback=None):
        """
        urlpath: /aaa/bb/cc (without host)
        """
        if self.bank.exists(urlpath):
            print 'existed'
            yield self.bank.get(urlpath)
        else:
            print 'not exist: %s' % urlpath
            print 'proxy target: %s' % host
            cache_url(host, urlpath, timeout)
            yield ""

    def update(self, host, urlpath, content=None, timeout=10, async=False):
        if content:
            pass
        else:
            query_url = self.get_query_url(host, urlpath) 
            if async:
                urlfetch(query_url, timeout, async=async)
                return
            else:
                content = urlfetch(query_url, timeout)

        self.bank.set(urlpath, content)

        return content

