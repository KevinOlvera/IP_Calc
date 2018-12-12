__author__ = 'Kevin Olvera'
import sys
import re

def _dec_to_binary(ip_address):
    return map(lambda x: bin(x)[2:].zfill(8), ip_address)


def _negation_mask(net_mask):
    wild = list()
    for i in net_mask:
        wild.append(255 - int(i))
    return wild


class IPCalculator(object):
    def __init__(self, ip_address, cdir=24):
        if '/' in ip_address:
            self._address_val, self._cidr = ip_address.split('/')
            self._address = map(int, self._address_val.split('.'))
        else:
            self._address = map(int, ip_address.split('.'))
            self._cidr = cdir
        self.binary_IP = _dec_to_binary(self._address)
        self.binary_Mask = None
        self.negation_Mask = None
        self.network = None
        self.broadcast = None

    def __repr__(self):
        print "\nCalculando el rango IP de %s/%s" % (".".join(map(str, self._address)), self._cidr)
        print "=============================================="
        ip = (".".join(map(str, self._address)))
        ip_check = ip.split('.')
        if int(ip_check[0]) < 128: 
            clase = 'A'
        elif int(ip_check[0]) < 192: 
            clase = 'B'
        elif int(ip_check[0]) < 224: 
            clase = 'C'
        elif int(ip_check[0]) < 240: 
            clase = 'D'
        elif int(ip_check[0]) < 256:
            clase = 'E'       
        print "Clase: " + clase
        print "Netmask %s" % (".".join(map(str, self.net_mask())))
        print "Network ID %s" % (".".join(map(str, self.network_ip())))
        print "Subnet Broadcast address %s" % (".".join(map(str, self.broadcast_ip())))
        print "Host range %s" % (self.host_range())
        print "Numero maximo de host %s" % (self.number_of_host())

    def net_mask(self):
        mask = [0, 0, 0, 0]
        for i in range(int(self._cidr)):
            mask[i / 8] += 1 << (7 - i % 8)
        self.binary_Mask = _dec_to_binary(mask)
        self.negation_Mask = _dec_to_binary(_negation_mask(mask))
        return mask

    def broadcast_ip(self):
        broadcast = list()
        for x, y in zip(self.binary_IP, self.negation_Mask):
            broadcast.append(int(x, 2) | int(y, 2))
        self.broadcast = broadcast
        return broadcast

    def network_ip(self):
        network = list()
        for x, y in zip(self.binary_IP, self.binary_Mask):
            network.append(int(x, 2) & int(y, 2))
        self.network = network
        return network

    def host_range(self):
        min_range = self.network
        min_range[-1] += 1
        max_range = self.broadcast
        max_range[-1] -= 1
        return "%s - %s" % (".".join(map(str, min_range)), ".".join(map(str, max_range)))

    def number_of_host(self):
        return (2 ** sum(map(lambda x: sum(c == '1' for c in x), self.negation_Mask))) - 2


def ip_calculate(ip):
    ip = IPCalculator(ip)
    ip.__repr__()

if __name__ == '__main__':
    ip = sys.argv[1] if len(sys.argv) > 1 else sys.exit(0)
    ip_calculate(ip)