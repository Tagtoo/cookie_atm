import redis
import urllib2
from multiprocessing import Process


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
        raise Exception("Not yet implemented.")


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

    def query(self, urlpath):
        """
        urlpath: /aaa/bb/cc (without host)
        """

        if self.bank.exists(urlpath):
            return self.bank.get(urlpath)
        else:
            query_url = "%s/%s" % (self.target_host, urlpath)
            req = urllib2.Request(query_url)

            with urllib2.urlopen(req) as url_res:
                content = url_res.read()

            self.bank.set(urlpath, content)
            return content

    def update(self, urlpath, content):
        raise Exception("Not yet implemented.")




