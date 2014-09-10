import itertools
import random
import socket
import webbrowser


def open_browser(ip, port):
    webbrowser.open('http://{0}:{1}'.format(ip, port))


def find_open_port(ip, port, n=50):
    """Find an open port near the specified port.

    Adapted from `mpld3._server`.
    """
    ports = itertools.chain((port + i for i in range(n)),
                            (port + random.randint(-2 * n, 2 * n)))

    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        s.close()
        if result != 0:
            return port
    raise ValueError("no open ports found")
