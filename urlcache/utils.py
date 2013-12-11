from urllib.parse import urlparse

def resolve_url(url):
    parse_result = urlparse(url)

def urlfetch(query_url):

    req = urllib2.Request(query_url)

    with urllib2.urlopen(req) as url_res:
        content = url_res.read()

    return content


