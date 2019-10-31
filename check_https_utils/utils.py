# coding: utf-8


__author__ = 'Catarina Silva'
__version__ = '0.1'
__email__ = 'c.alexandracorreia@ua.pt'
__status__ = 'Development'


import sys
import socket
import pickle


def send_msg(sock, msg, addr):
    data = pickle.dumps(msg)
    l = len(data)
    sock.sendto(str(l).encode(), addr)
    sock.sendto(data, addr)


def recv_msg(sock):
    l, addr = sock.recvfrom(4)
    l = int(l.decode('utf-8'))
    data, addr = sock.recvfrom(l)
    return pickle.loads(data), addr


def progress_bar(count, total, status='', bar_len=60):
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
