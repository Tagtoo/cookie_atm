PROXIED_URLS = [
    "/hello",
    "/local.html",
    "/hello3"
]

"""
Special proxy setting for perticular routes
"""
SPECIAL_ROUTES = {
    '/hello4': 'http://localhost:5001',
    '/hello5': 'http://localhost:5000'
}

"""
Special timeout setting for perticular routes
"""
SPECIAL_TIMEOUTS = {
    '/hello4': 10
}

DEFAULT_TIMEOUT = 2

DEFAULT_PROXIED_HOST = "http://localhost:8000"

try:
    from atm_settings_local import *
except:
    pass

