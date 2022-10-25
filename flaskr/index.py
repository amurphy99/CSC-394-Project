
from flask import Flask, render_template, g, request, flash
from flaskr.db import get_database_connection
from flaskr.db import get_db



#@app.route('/index', methods=('GET', 'POST'))
def index():
    '''
    variables for admin_index.html
    userID = the ID of the user who is being modifies
    action = the action being taken 
        5 = delete user 
        6 = confirm delete user
        1 = load password reset form
        2 = submit password reset
        3 = promote user to admin
        4 = demote user 
        7 = show new user creation fields
        8 = create new user from given info
    '''
    # initialize the variables
    userID          = -1
    action          = -1
    new_password    = "NONE"
    new_username    = "NONE"

    # Perform action and reload the page
    # ------------------------------------
    if request.method == 'POST':
        userID = int(request.form["modify_userID"])
        action = int(request.form["action"])
        
        # delete user / confirm delete user
        # -----------------------------------
        if   action == 5: pass # reload page with "confirm delete user" button
        elif action == 6:
            # SQL goes here
            # - remove user from database
            db  = get_db()
            cur = db.cursor()

            cur.execute(f"DELETE FROM test_user WHERE id = '{userID}'")
            db.commit()

            cur.close()
            db.close()
            
        
        # Change the userID's password to the newly submitted one
        # --------------------------------------------------------
        elif action == 1: pass # reload page with reset password form
        elif action == 2:
            if "new_password" in request.form: # shouldnt need this, but just in case
                new_password = request.form["new_password"]
                # SQL goes here
                # - change the password for userID to be new_password
                db  = get_db()
                cur = db.cursor()

                cur.execute( f"UPDATE test_user set password = '{new_password}' WHERE id = '{userID}'" )
                db.commit()

                cur.close()
                db.close()

        # promote user
        # -------------
        elif action == 3:
            # SQL goes here
            # change userIDs privileges to 1
            db  = get_db()
            cur = db.cursor()

            cur.execute( f"UPDATE test_user SET privileges = {1} WHERE id = '{userID}'" )
            db.commit()

            cur.close()
            db.close()

        # demote user 
        # ------------
        elif action == 4:
            #if int(userID) == 0: pass # (protection to prevent "admin" from getting demoted)
            # SQL goes here
            # change userIDs privileges to 0
            db  = get_db()
            cur = db.cursor()

            cur.execute( f"UPDATE test_user SET privileges = {0} WHERE id = '{userID}'" )
            db.commit()

            cur.close()
            db.close()

        # create new user (should probably add protections for using the same username twice)
        # -----------------------------------------------------------------------------------
        elif action == 7: pass # reload page with new user form
        elif action == 8:
            if "new_password" in request.form and "new_username" in request.form: # shouldnt need this, but just in case
                new_password = request.form["new_password"]
                new_username = request.form["new_username"]
                # SQL goes here
                db    = get_db()
                error = None

                if   not new_username: error = 'Username is required.'
                elif not new_password: error = 'Password is required.'

                if error is None:
                    try:
                        cur = db.cursor()
                        cur.execute( f"INSERT INTO test_user (username, password) VALUES ('{new_username}', '{new_password}')" )
                        db.commit()
                        cur.close()
                    except db.IntegrityError:
                        error = f"User {new_username} is already registered."
                        flash(error)
                else:
                    flash(error)

    # showing this at the top of the page right now to help with debugging
    debug_info = f"ID: {userID}    |    ACTION: {action}    |    NEW_PASSWORD: {new_password}    |    NEW_USERNAME: {new_username}"


    # Get user info for the actual page
    # -----------------------------------
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_user;")
    test_users = cur.fetchall()
    cur.close()
    conn.close()


    # Return the correct page to the user
    # -------------------------------------
    # check if the user is logged in and has admin privelages, if so, show them admin view
    if g.user != None:
        if g.user[3] == 1:
            return render_template('admin_index.html', test_users=test_users, userID=userID, action=action, debug_info=debug_info)

    # otherwise, show them the regular user version of the page
    return render_template('index.html', test_users=test_users)