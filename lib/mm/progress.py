"""Progress status and indicator classes."""

import socket
import struct
import sys
import traceback

MESSAGE_PREFIX_FORMAT = "=HQ"
"""Message prefix pack/unpack format."""

MESSAGE_PREFIX_SIZE = struct.calcsize(MESSAGE_PREFIX_FORMAT)
"""Bytes in prefix."""

STATUS_FORMAT = "=HHHhh"
"""Repeating status item format."""

STATUS_SIZE = struct.calcsize(STATUS_FORMAT)
"""Bytes in a status segment"""

NAME_LENGTH_FORMAT = "=h"
"""Encoding of name length."""

NAME_LENGTH_SIZE= struct.calcsize(NAME_LENGTH_FORMAT)
"""Bytes in name length."""

NAME_FORMAT_TEMPLATE = "={}s"

class CalculationStatus(object):
    """Maintains counters indicating that allow esimation of progress of a tree
    calculation."""

    def __init__(self, parent, problem_size, **kwargs):
        """:param parent: Parent calculation status.
        :param problem_size: size of the problem being calculated.
        :param kwargs: misc keyword arguments, for future use.
        """

        self.parent = parent
        """Parent calculation status."""

        self.problem_size = problem_size
        """Problem size."""

        self.candidate_count = 0
        """Number of candidates considered for this problem."""

        self.child_count = 0
        """Number of child problems under the current candidate."""

        self.cur_candidate = -1
        """Index of current candidate."""

        self.cur_child = -1
        """Index of current problem being solved."""


    def next_candidate(self, pr):
        """:param pr: next candidate under consideration.

        This call advances the candidate index, and resets the subproblem
        progress status.
        """
        self.cur_candidate += 1
        self.child_count = pr.stats.n
        self.cur_child = -1


    def make_message(self, total, name):
        """Create a bytearry encoding progress status, total entries into recursive solver, 
        and the name of the problem being solved.

        :param total: number of entries in recursive solver.
        :param name: identifies the problem.
        :return: a byte array.
        """
        n = 1
        p = self
        while p.parent:
            n += 1
            p = p.parent

        msg_size = MESSAGE_PREFIX_SIZE + n * STATUS_SIZE + NAME_LENGTH_SIZE + len(name)
        msg = bytearray(msg_size)
        offset = 0

        struct.pack_into(MESSAGE_PREFIX_FORMAT, msg, offset, n, total)
        offset += MESSAGE_PREFIX_SIZE

        name_length = len(name)
        struct.pack_into(NAME_LENGTH_FORMAT, msg, offset, name_length)
        offset += NAME_LENGTH_SIZE

        struct.pack_into(NAME_FORMAT_TEMPLATE.format(name_length), msg, offset, name)
        offset += name_length

        p = self
        while p:
            struct.pack_into(STATUS_FORMAT, msg, offset,
                             p.problem_size, p.candidate_count, p.child_count, 
                             p.cur_candidate, p.cur_child)
            offset += STATUS_SIZE
            p = p.parent

        return msg


    def to_string(self):
        return "size={} candidates={}/{} children={}/{}".format(
            self.problem_size, self.cur_candidate, self.candidate_count, 
            self.cur_child, self.child_count)
        

    def __repr__(self):
        return "{}({})".format(super(CalculationStatus, self).__repr__(), self.to_string())


    @staticmethod
    def read_message(sock):
        """Reads a message from the socket, and parses it into its components.

        :param sock: datagram socket to read from.
        :return: see :py:meth:`.CalculationResult.parse_message`.
        """
        try:
            msg = sock.recv(4096)
            return CalculationStatus.parse_message(msg)
        except socket.error:
            return None


    @staticmethod
    def parse_message(msg):
        """Parses byte arrary into progress data

        :param msg: byte array.
        :return: a tuple  *(N, total, name, chain)*.
          - N: number of elements in *chain*.
          - total: total operation count.
          - name: an identifier associated with the progress message.
          - chain: list of status indicators from bottom to top of recursion stack.
        """

        offset = 0
        (n, total) = struct.unpack_from(MESSAGE_PREFIX_FORMAT, msg, offset)
        offset += MESSAGE_PREFIX_SIZE

        (name_length,) = struct.unpack_from(NAME_LENGTH_FORMAT, msg, offset)
        offset += NAME_LENGTH_SIZE

        (name,) = struct.unpack_from(NAME_FORMAT_TEMPLATE.format(name_length), msg, offset)
        offset += name_length

        chain = []
        for _ in xrange(n):
            data = struct.unpack_from(STATUS_FORMAT, msg, offset)
            offset += STATUS_SIZE

            node = CalculationStatus(None, data[0])
            node.candidate_count, node.child_count, node.cur_candidate, node.cur_child = \
                data[1:]
            chain.append(node)

        for i in xrange(n-1):
            chain[i].parent = chain[i+1]

        return (n, total, name, chain)


class ReportingCalculationStatus(CalculationStatus):
    """A calculation status with the ability to report its contents
    through a unix datagram socket."""

    UNIX_PREFIX = 'unix://'
    IP_PREFIX = 'ip://'

    DELIMITER = '/'

    def __init__(self, *args, **kwargs):
        """
        :param root_ctx: root problem definition, used to instanite the top
          level status object.
        """
        self.name = '<unnamed>'
        self.root_ctx = kwargs.get('root_ctx')
        super(ReportingCalculationStatus, self).__init__(*args, **kwargs)
        self._initsock()


    def _initsock(self):
        if self.parent:
            self._sock = self.parent._sock
            self._sockaddr = self.parent._sockaddr
            self.name = self.parent.name
            return

        self._sock = None
        self._sockaddr = None

        sockname = self.root_ctx.status_socket
        if sockname.find(self.UNIX_PREFIX) == 0:
            family = socket.AF_UNIX
            (name, sockname) = sockname[len(self.UNIX_PREFIX):].split(self.DELIMITER, 1)
        elif sockname.find(self.IP_PREFIX) == 0:
            family = scoket.AF_INET
            (name, sockname) = sockname[len(self.IP_PREFIX)].split(self.DELIMITER, 1)
            (host, port) = sockname[len(self.IP_PREFIX):].split(':')
            sockname = (socket.gethostbyname(host), port)
        else:
            raise ValueError("Unrecognized address schema: '{}'".format(sockname))

   
        sock = socket.socket(family, socket.SOCK_DGRAM)
        sock.setblocking(0)

        self._sock = sock
        self._sockaddr = sockname
        self.name = name


    def report(self, total):
        """:param total: Total operation count; number of times recursive solver was entered.

        This method packs the current status into a network message, and sends it over the
        Unix datagram socket associated with this instance.

        The message consists of a prefix followed by repeating status segments.  The status
        elements are from the bottom to the top, with the root problem at the end.

        The packed formatting follows this grammar:

        .. code-block:: none

            <format> ::=  <N> <total> <name> <status>{N}
                          =H =Q
            <name>   ::=  <length> <char>{<length>}
                          =H      =s (with a count)
            <status> ::=  <prob_size><n_cand><n_child><cur_cand><cur_child>
                          =H        =H     =H      =h       =h
            N: number of <status> segments.
            total: total number of recursive solver entries.
            prob_size: problem size.
            n_cand: number of canidates.
            n_child: number of children, or subproblems.
            cur_cand: current candidate index (0-based).
            cur_child: current child index (0-based).
        """
        msg = self.make_message(total, self.name)
        self._send_message(msg)


    def _send_message(self, msg):
        try:
            self._sock.sendto(msg, self._sockaddr)
        except socket.error:
            pass
