from flask import Flask, render_template, g, request, flash
from flaskr.db import get_database_connection
from flaskr.db import get_db



#@app.route('/user/<userID>', methods=('GET', 'POST'))
def user_page(userID):

    # get info from database
    # -----------------------
    db  = get_db()
    cur = db.cursor()

    cur.execute( f"SELECT * FROM test_user WHERE id = '{userID}';" )
    this_user = cur.fetchone()

    cur.execute( f"SELECT * FROM movies_list_info WHERE owner_id = '{userID}';" )
    user_lists = cur.fetchall()

    cur.close()
    db.close()


    return render_template('user_page/user_page.html', this_user=this_user, user_lists=user_lists)

