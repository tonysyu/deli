"""
A Simple server used to show deli images.
"""
import flask

from .flask_utils import open_app


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
    def server():
        return flask.render_template(template, data=data)
    app.add_url_rule(url, view_func=server)


def show():
    open_app(app)
