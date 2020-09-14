from pvr.recorder import Recorder
import sys

def main():
    recorder = Recorder(url='http://localhost:8000', client_secret='sample-client-secret')
    resp = recorder.start('stream','admin@example.com','input','output',333)
    print(resp["data"]["stream"]["id"])
    return 0



if __name__ == '__main__':
  sys.exit(main())
