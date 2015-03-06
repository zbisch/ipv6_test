from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import task
from twisted.web.resource import Resource
from twisted.web import server, resource

def start_consumers(q):
    def consumer(info):
        q.get().addCallback(consumer)
        if 'port' in info.args:
            try:
                port = int(info.args['port'][0])
                try_connection(info.client.host, port)
            except:
                return
    q.get().addCallback(consumer)


def try_connection(host, port):
    print host, port
    pass


class Hello(Resource):
    isLeaf = True
    def render_GET(self, request):
        return ""

    def render_POST(self, request):
        q.put(request)
        return ""

q = defer.DeferredQueue()
start_consumers(q)

resource =  server.Site(Hello())
reactor.listenTCP(8080, resource)
reactor.run()

