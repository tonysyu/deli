"""
A Simple server used to show deli images.
"""
import webbrowser
import socket
import itertools
import random

from flask import Flask, render_template

app = Flask(__name__)


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


def serve_and_open(html, ip='127.0.0.1', port=8888, n_retries=50, debug=False):
    """Start a server serving the given HTML, and open a browser

    Parameters
    ----------
    html : str
        HTML to serve
    ip : string (default = '127.0.0.1')
        IP address at which the HTML will be served.
    port : int
        The port at which to serve the HTML
    n_retries : int
        The number of nearby ports to search if the specified port is in use.
    debug : bool
        Run app in debug-mode. Note that this causes two tabs to open up.
    """
    port = find_open_port(ip, port, n_retries)

    @app.route('/')
    def server():
        return render_template('base.html', content=html)

    open_browser(ip, port)
    app.run(host=ip, port=port, debug=debug)


if __name__ == '__main__':
    serve_and_open('Hello')
