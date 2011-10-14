from twisted.internet import reactor, endpoints, protocol
import socks
import pdb

from twisted.web._newclient import Request
from twisted.web.http_headers import Headers

def quickHTTP(host, method, path):
    headers = Headers()
    headers = Headers(dict(headers.getAllRawHeaders()))
    headers.addRawHeader('host', host)
    return Request(method, path, headers, None)

def bind():
    factory = socks.SOCKSv4ClientFactory(reactor)
    point = endpoints.TCP4ClientEndpoint(reactor, "localhost", 1080)
    d = point.connect(factory)

    def connected(p):
        d = p.sendBind("localhost", 3000, "peter")
        d.addBoth(lambda x: pdb.set_trace())

    d.addCallbacks(connected, lambda x: pdb.set_trace())

def connect():
    factory = socks.SOCKSv4ClientFactory(reactor)
    point = endpoints.TCP4ClientEndpoint(reactor, "localhost", 1080)
    d = point.connect(factory)

    def connected(p):
        d = p.sendConnect("example.com", 80, "peter")
        p.sendConnect("example.com", 80, "peter")
        r = quickHTTP('example.com', 'GET', '/')
        d.addCallback(lambda x: p.sendConnect("example.com", 80, "peter"))
        d.addBoth(lambda x: r.writeTo(p.transport))

    d.addCallbacks(connected, lambda x: pdb.set_trace())

if __name__ == "__main__":
    print 'CONNECT TEST'
    connect()
    print 'BIND TEST'
    bind()
    reactor.run()
