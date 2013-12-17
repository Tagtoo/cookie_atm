from urlparse import urlparse
import urllib2

def resolve_url(url):
    parse_result = urlparse(url)

def urlfetch(query_url):
    req = urllib2.Request(query_url)

    url_res = urllib2.urlopen(req)
    content = url_res.read()

    return content


