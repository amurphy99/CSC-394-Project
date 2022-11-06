from flask import Flask, render_template, g, request, flash
from flaskr.db import get_database_connection
from flaskr.db import get_db







#@app.route('/index_htmx', methods=('GET', 'POST'))
def index_htmx():

    # Get user info for the actual page
    # -----------------------------------
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM all_users;")
    test_users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("index_htmx/index_htmx.html", test_users=test_users, userID=-1, action=-1)




#@app.route('/reset_password_htmx', methods=('POST'))
def reset_password_htmx():
    # Always given this information
    this_user = request.form["this_user"]

    # Check which version sent the POST
    if "new_password" in request.form:
        new_password = request.form["new_password"]

        # SQL goes here -> change the password for userID to be new_password
        # --------------
        db = get_db(); cur = db.cursor()
        cur.execute( f"UPDATE test_user SET password = '{new_password}' WHERE id = '{this_user[0]}'" ); db.commit()
        cur.close(); db.close()

        # return the base page
        return render_template("index_htmx/reset_password_htmx.html", this_user=this_user)

    # Show the new password form
    elif "action" in request.form:
        return render_template("index_htmx/confirm_new_password_htmx.html", this_user=this_user)

    # Page was loaded from another way
    else:
        return render_template("index_htmx/reset_password_htmx.html", this_user=this_user)









