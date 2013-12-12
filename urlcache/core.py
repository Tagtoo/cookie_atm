import redis
import urllib2
from multiprocessing import Process
from utils import urlfetch


class RedisBank(object):
    def __init__(self, host='localhost'):
        self.pool = redis.ConnectionPool(host=host)
        self.redis_client = redis.Redis(connection_pool=self.pool)

    def set(self, key, value, blocking=True):
        if blocking:
            self.redis_client(key, value)
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
    def __init__(self, target_host, bank):
        self.target_host = target_host
        self.bank = bank

    def get_query_url(self, urlpath):
        return "%s/%s" % (self.target_host, urlpath)


    def query(self, urlpath):
        """
        urlpath: /aaa/bb/cc (without host)
        """

        if self.bank.exists(urlpath):
            return self.bank.get(urlpath)
        else:
            query_url = self.get_query_url(urlpath)
            content = urlfetch(query_url)
            self.bank.set(urlpath, content)
            return content

    def update(self, urlpath, content=None):

        if content:
            query_url = self.get_query_url(urlpath) 
            content = urlfetch(query_url)
        else:
            pass


        self.bank.set(urlpath, content)

        return content
        





