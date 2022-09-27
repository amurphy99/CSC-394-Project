import os

from flask import Flask



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # things added from later steps in the tutorial
    # ------------------------
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    # created function for handling the index page (stored in another file)
    # ---------------------------------------------
    from . import index
    app.add_url_rule('/index', methods=('GET', 'POST'), view_func=index.index)

    from . import test
    app.add_url_rule('/test1', methods=('GET', 'POST'), view_func=test.test1)
    app.add_url_rule('/test2', methods=('GET', 'POST'), view_func=test.test2)

    return app