from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher


import requests
import json


@dispatcher.add_method
def foobar(self, **kwargs):
    return kwargs["foo"] + kwargs["bar"]


@Request.application
def application(request):
        # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["ping"] = lambda: True
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


class DummyPyService(object):
    """docstring for dummy_py_service"""

    def __init__(self, hub_url='http://localhost:8080', config='conf'):
        super(DummyPyService, self).__init__()
        self.hub = hub_url
        self.name = 'dummy python'
        self.config = config
        self.id = str(0)
        self.headers = {'content-type': 'application/json'}
        self.info = 'info'
        self.__call('attachService', dict(serviceName=self.name,
                                          info=self.info, config=self.config))
        run_simple(self.config['host'], self.config['port'], application)

    def __call(self, methodname, params):
        payload = {
            "method": methodname,
            "params": params,
            "jsonrpc": "2.0",
            "id": self.id,
        }
        response = requests.post(
            self.hub, data=json.dumps(payload), headers=self.headers).json()
        print(response)
        bolean = False
        return bolean

    def getServices(self):
        return False

    def doServiceExists(self):
        return False


if __name__ == "__main__":
    config = {'port': 8088, 'host': '127.0.0.1', 'path': '/', 'strict': True}
    hub_url = 'http://localhost:8080'
    service = DummyPyService(config=config, hub_url=hub_url)
