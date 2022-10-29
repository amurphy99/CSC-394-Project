from flask import Flask, render_template, g, request, flash, session
from flaskr.db import get_database_connection
from flaskr.db import get_db



#@app.route('/user/<userID>', methods=('GET', 'POST'))
def user_page(userID):
    '''
    GET request only

    takes:
        * userID

    returns:
        * user_info
        * statistics
        * user_lists
    
    '''

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

    statistics = [  ("Joined:",             str(this_user[4])[:10]  ),
                    ("Movies Completed:",   123                     ), 
                    ("Currently Watching:", 3                       ), 
                    ("Plan to Watch:",      12                      ),
                    ("Watch Time:",         "24d 05h 22m"           )   ]

    return render_template('user_page/user_page.html', this_user=this_user, user_lists=user_lists, statistics=statistics)





#@app.route('/new_list_modal', methods=('POST'))
def new_list_modal():
    return render_template('user_page/new_list_modal.html')





# app.add_url_rule('/user/create_new_list', methods=('GET', 'POST'), view_func=user_page.create_new_list)
def create_new_list():

    # make sure to double check the user is logged in
    if g.user == None:
        error = 'Error: not logged in'
        flash(error)
        return

    # create the new watch list
    if request.method == 'POST':
        new_title   = str(request.form["new-list-title"])
        new_desc    = str(request.form["new-list-description"])
        userID      = int(request.form["userID"])


        db = get_db(); cur = db.cursor()

        cur.execute( f"INSERT INTO movies_list_info (owner_id, list_name, list_description) VALUES ({userID}, '{new_title}', '{new_desc}') RETURNING *;" )
        db.commit()
        new_list = cur.fetchone()
        
        cur.close(); db.close()


        return render_template('user_page/list_created_htmx.html', new_list=new_list)


    return



