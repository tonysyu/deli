from deli.app.js.utils import find_open_port, open_browser


def open_app(app, ip='127.0.0.1', port=8888, n_retries=50, debug=False):
    """Start a server serving the given HTML, and open a browser

    Parameters
    ----------
    data : anything
        Data sent to rendered template.
    ip : string (default = '127.0.0.1')
        IP address at which the HTML will be served.
    port : int
        The port at which to serve the HTML
    n_retries : int
        The number of nearby ports to search if the specified port is in use.
    debug : bool
        Run app in debug mode. Note that debug mode causes two tabs to open up.
    """
    port = find_open_port(ip, port, n_retries)

    open_browser(ip, port)
    app.run(host=ip, port=port, debug=debug)
