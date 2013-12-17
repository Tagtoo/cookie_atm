PROXIED_URLS = [
    "/hello",
    "/local.html",
    "/hello3"
]

SPECIAL_ROUTES = {
    '/hello4': 'http://localhost:5001',
    '/hello5': 'http://localhost:5000'
}

DEFAULT_PROXIED_HOST = "http://localhost:8000"

try:
    from atm_settings_local import *
except:
    pass

