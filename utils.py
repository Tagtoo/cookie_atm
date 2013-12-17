
class Router(object):
    def __init__(self, routes={}):
        self.routing_table = {}
        
    def add_route(self, path, host):
        path = self.parse_path(path)
        self.routing_table[path] = host

    def get_route(self, path):
        path = self.parse_path(path)
        return self.routing_table[path]

    def exist_route(self, path):
        path = self.parse_path(path)
        return path in self.routing_table

    def parse_path(self, url_with_argument):
        if '?' in url_with_argument:
            return url_with_argument.split('?')[-1]
        else:
            return url_with_argument
