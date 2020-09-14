import requests
from django.conf import settings

class Recorder(object):
      
    def __init__(self, url=settings.RECORDER_URL, client_secret=settings.RECORDER_CLIENT_SECRET):
        self.base_url = url
        self.secret = client_secret

    def request_url(self, path):
        return self.base_url + path

    def start(self, stream_name, owner_email, input_url, output_url, max_duration):
        url = self.request_url('/api/v1/stream/')
        print(url)
        req_data = {
        'stream_name': stream_name,
        'user_email': owner_email,
        'input_url': input_url,
        'output_url': output_url,
        'max_duration': max_duration
        }       
        resp = requests.post(url, json=req_data, headers={ 'Content-Type':'application/json', 'Authorization': self.secret })
        if resp.status_code != 201:
            raise Exception('Unable to start recording: {:d}'.format(resp.status_code))
        return resp.json()


    def stop(self, recording_id):
        url = self.request_url('/api/v1/stream/{:d}'.format(recording_id))
        print(url)
        resp = requests.put(url,headers={'Authorization': self.secret})
        if resp.status_code != 204:
            raise Exception('Unable to stop recoding: {:d}'.format(resp.status_code))
        return True


    def remove(self, recording_id):
        url = self.request_url('/api/v1/stream/{:d}'.format(recording_id))
        print(url)
        resp = requests.delete(url,headers={'Authorization': self.secret})
        if resp.status_code != 204:
            raise Exception('Unable to stop recoding: {:d}'.format(resp.status_code))
        return True
