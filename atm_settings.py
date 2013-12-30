"""
default settings template
"""
PROXIED_URLS = [
    "/hello",
    "/local.html",
    "/hello3",
    "/test"
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

REDIS_CONN_MAX = 50

TEST = False


"""
if atm_settings_local.py exists, we could overwrite the setting with this
"""
try:
    from atm_settings_local import *
except:
    pass

"""
import test setting if the test flag set to True
"""
if TEST:
    from atm_settings_test import *
