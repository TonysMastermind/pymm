from mm import *
from mm.progress import CalculationStatus
from mm.partition import PartitionResult

import os
import os.path
import socket
import traceback

def test():
    c = CalculationStatus(None, 1296)
    pr = PartitionResult(CODETABLE.ALL, 8)
    c.next_candidate(pr)
    cc = CalculationStatus(c, len(pr.parts[11]))
    m = cc.make_message(100, "TESTING")

    print m

    (n, total, name, chain) = cc.parse_message(m)
    print (n, total, name, chain)
    for c in chain:
        print c.to_string()

def main():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    if os.path.exists('PROGRESS'):
        os.remove('PROGRESS')

    s.bind('PROGRESS')
    s.setblocking(1)

    while True:
        msg = s.recv(4096)

        try:
            (n, total, name, chain) = CalculationStatus.read_message(s)

            print "----"
            print n, total, name
            for c in chain:
                print c.to_string()
        except:
            traceback.print_exc()


if __name__ == '__main__':
    main()
