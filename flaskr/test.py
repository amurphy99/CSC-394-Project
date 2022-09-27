
from flask import Flask, render_template, g, request, flash
from flaskr.db import get_database_connection
from flaskr.db import get_db


#@app.route('/test1', methods=('GET', 'POST'))
def test1():
    hidden_val = 0

    # Get user info for the actual page
    # -----------------------------------
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_user;")
    test_users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('test.html', test_users=test_users, hidden_val=hidden_val)


def test2():
    # 0 = red
    # 1 = blue
    color = int(request.form["new_color"])

    if color == 1:
        return '<div style="background:red" > Red </div>'

    elif color == 0: 
        return '<div style="background:blue" > Blue </div>'
    
    else:
        return '<div style="background:green" > Green </div>'

