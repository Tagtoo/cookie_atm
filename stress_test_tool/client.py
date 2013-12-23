#!/usr/bin/env python
"""
Testing client for testing cookie bank
"""
from tornado.httpclient import HTTPRequest
from tornado import httpclient

import test_pb2

TEST_HOST = "localhost"
TEST_MESSAGE = {
    'person': {
        'name': 'Colin Su',
        'id': 12345,
        'email': 'littleq0903@gmail.com'
        }
    }

def send_message(url, body=None, method='GET', handler=None):
    """
    if handler == None: send a sync request
    else handler == <function>: send async request
    """
    request = HTTPRequest(url, method=method)
    if body:
        request.body = body

    if handler:
        httpclient.AsyncHTTPClient(request, handler)
    else:
        client = httpclient.HTTPClient()
        response = client.fetch(request)
        return response.body

def proto_encode(obj):
    person_obj = obj['person']
    person = test_pb2.Person()
    
    person.name = person_obj['name']
    person.id = person_obj['id']
    person.email = person_obj['email']

    return person.SerializeToString()

def proto_decode(s):
    person = test_pb2.Person()
    person.ParseFromString(s)
    return person

def main():
    test_path = "/test"
    test_url = "http://%s%s" % ( TEST_HOST, test_path )

    encoded = proto_encode(TEST_MESSAGE)

    # set value
    send_message(test_url, method='POST', body=encoded)
    received = send_message(test_url)

    print proto_decode(received)


if __name__ == '__main__':
    main()
