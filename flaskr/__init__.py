import os

from flask import Flask, render_template



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

    from . import index_htmx
    app.add_url_rule('/index_htmx',             methods=('GET', 'POST'), view_func=index_htmx.index_htmx         )
    app.add_url_rule('/reset_password_htmx',    methods=('GET', 'POST'), view_func=index_htmx.reset_password_htmx)

    from . import watch_list
    app.add_url_rule('/watch_list/<listID>',    methods=('GET', 'POST'), view_func=watch_list.watch_list)

    from . import user_page
    app.add_url_rule('/user/<userID>',           methods=('GET', 'POST'), view_func=user_page.user_page)

    # a simple page that says hello
    @app.route('/test3')
    def test3():
        return render_template('test2.html')

    from . import movieDBapi
    app.add_url_rule('/api_testing',        methods=('GET', 'POST'), view_func=movieDBapi.api_testing)
    app.add_url_rule('/send_query_htmx',    methods=('GET', 'POST'), view_func=movieDBapi.get_results)




    return app