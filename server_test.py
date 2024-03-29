#! /usr/bin/python
from twisted.internet import reactor, protocol
import socks


class SOCKSv4Factory(protocol.Factory):
    def __init__(self, log):
        self.logging = log

    def buildProtocol(self, addr):
        return socks.SOCKSv4(self.logging, reactor)

if '__main__' == __name__:
    reactor.listenTCP(1080, SOCKSv4Factory("socks.log"))
    reactor.run()
