from urlparse import urlparse
import urllib2

def resolve_url(url):
    parse_result = urlparse(url)

def urlfetch(query_url, timeout):
    req = urllib2.Request(query_url)

    url_res = urllib2.urlopen(req, timeout=timeout)
    content = url_res.read()

    return content


