#!/usr/bin/env python 

## Google APIs
# apiclient
from apiclient.discovery import build

# Oauth2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

# Python Built-in Libraries
import httplib2
import trackback

__author__ = "Colin Su <littleq@tagtoo.org>"




default_settings = {
    'instance_settings': {
        'zone': 'us-central1-a',
        'image': 'debian',
        'images': {
            'debian': 'debian-7-wheezy-v20131119',
            'centos': 'centos-6-v20131119'
        },
        'machine_type': 'debian'
        'instance_name_prefix': 'tagtoo-'
    },
    'project_settings': {
        'gce_scopes': [
            'https://www.googleapis.com/auth/compute'
        ],
        'gce_api_version': 'v1',
        'gce_url': 'https://www.googleapis.com/compute/%s/projects/' % (default_settings['gce_api_version'])
        'oauth2_storage': 'oauth2.dat',
        'client_secrets': 'client_secrets.json',
        'project_id': '',
    }
}

settings = default_settings.copy()

try:
    from custom_settings import custom_settings
except:
    custom_settings = None

if custom_settings:
    print "Custom settings detected!"
    settings.update(custom_settings)

class GCEService(object):
    def __init__(self, project_settings, auth_http, project_id, blocking=True):
        self.project_settings = project_settings
        self.service = build('compute', settings['gce_api_version']) 
        self.auth_http = self.get_authed_http()
        self.project_id = project_id
        self.project_url = "%s%s" % (settings['gce_url'], self.project_id)
        self.blocking = blocking

    def get_authed_http(self):
        """
        Get authed http client
        """
        flow = flow_from_clientsecrets(self.project_settings['client_secrets'], scope=self.project_settings['gce_scopes'])
        storage = Storage(self.project_settings['oauth2_storage'])
        credentials = storage.get()

        if not credentials or credentials.invalid:
            credentials = run(flow, storage)

        http = httplib2.Http()
        auth_http = credentials.authorize(http)

        return auth_http

    def execute(request):
        try:
            response = request.execute(self.auth_http)
        except:
            print 'unexpected error occured.'
            trackback.print_exc()
            return
            
        return response

    def list_instances(self):
        request = self.service.instances().list(project=self.project_id)


        

class GCEInstance(object):
    def __init__(self, service, settings, instance_name=None):
        self.gce_service = service
        self.instance_settings = settings
        self.instance_name = instance_name



if __name__ == '__main__':
