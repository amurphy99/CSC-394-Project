import os

# Need to figure out how to write the code for pages in other files
# (the import for g and request won't be needed then)
from flask import Flask, render_template, g, request
from flaskr.db import get_database_connection



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

    # my testing stuff 
    @app.route('/index', methods=('GET', 'POST'))
    def index():
        '''
        variables for admin_index.html
        userID = the ID of the user who is being modifies
        action = the action being taken 
            0 = delete user 
            1 = load password reset form
            2 = submit password reset
            3 = change their privileges
        
        '''
        # initialize the variables
        userID          = -1
        action          = -1
        new_password    = "NONE"

        # checking if it gets the right user
        if request.method == 'POST':
            userID = request.form["modify_userID"]
            action = request.form["action"]
            
            # promote or demote user
            if action == 3:
                # SQL goes here
                pass

            # reload page with reset password form
            elif action == 1:    
                pass

            # Change the userID's password to the newly submitted one
            elif action == 2:
                new_password = ["new_password"]
                # SQL goes here
                pass

        debug_info = f"ID: {userID} | ACTION: {action} | NEW_PASSWORD: {new_password}"




        # get all users info
        conn = get_database_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM test_user;')
        test_users = cur.fetchall()
        cur.close()
        conn.close()
        
        # check if the user is logged in and has admin privelages, if so, show them admin view
        if g.user != None:
            if g.user[3] == 1:
                return render_template('admin_index.html', test_users=test_users, debug_info=debug_info, action=action)

        # otherwise, show them the regular user version of the page
        return render_template('index.html', test_users=test_users)


    # things added from later steps in the tutorial
    # ------------------------
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    #from . import users
    #app.register_blueprint(users.bp)

    return app