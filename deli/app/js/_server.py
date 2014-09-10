"""
A Simple server used to show deli images.
"""
import flask

from deli.app.js.utils import find_open_port, open_browser


# Set the project root directory as the static folder.
app = flask.Flask(__name__, static_url_path='')


@app.route('/static/flot/<path:filename>')
def send_flot_files(filename):
    return flask.send_from_directory('static/flot', filename)


@app.route('/static/css/<path:filename>')
def send_css_files(filename):
    return flask.send_from_directory('static/css', filename)


def create_plot(data, url='/', template='base.html'):
    """Create web page displaying the given data and route the given URL there.
    """
    @app.route(url)
    def server():
        return flask.render_template(template, data=data)
    return server


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


if __name__ == '__main__':
    import numpy as np
    x = np.linspace(0, 10)
    data = np.transpose([x, np.sin(x)]).tolist()

    # Why doesn't the result need to be saved to prevent garbage collection?
    create_plot(data)
    open_app(app)
