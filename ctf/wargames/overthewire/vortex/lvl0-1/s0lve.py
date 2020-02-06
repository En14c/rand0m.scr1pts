#!/usr/bin/env python2

import sys
import socket
import struct


class Solve:
    def __init__(self, port, hostname):
        self.port = port
        self.hostname = hostname

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host_ip = socket.gethostbyname(self.hostname)
            self._socket.connect((self.host_ip, self.port))
        except socket.gaierror:
            print("Error establishing connection")
            sys.exit(-1)

    def _solve(self):
        _ret  = self._socket.recv(1024)
        print(len(_ret))

        # get tuple of 4 unsigned integers
        ints = struct.unpack("<IIII", _ret)
        ints_sum = struct.pack(
            "<Q", ints[0] + ints[1] + ints[2] + ints[3])
        self._socket.send(ints_sum)
        result = self._socket.recv(1024)
        print(str(result))

s = Solve(5842, 'vortex.labs.overthewire.org')
s._solve()
            




