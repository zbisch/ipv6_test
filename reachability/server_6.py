import flask
from flask import Flask
from flask import request

from twisted.internet import defer

def start_consumers(q):
    def consumer(info):
        q.get().addCallback(consumer)
        """
        if 'port' in info.args:
            try:
                port = int(info.args['port'][0])
                try_connection(info.client.host, port)
            except:
                return
        """
        if info.form and 'port' in info.form:
            ip = info.remote_addr
            port = info.form['port']
            print "HAVE A PORT:", ip, port
    q.get().addCallback(consumer)

q = defer.DeferredQueue()
start_consumers(q)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    q.put(request)
    return 'Success'

if __name__ == '__main__':
    #app.run()
   # app.run(host='0.0.0.0', port=port, debug=True)
    app.run(host='::', port=18106, debug=True)
