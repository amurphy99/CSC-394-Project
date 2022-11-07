from flask import Flask, render_template, g, request, flash, session

from flaskr.db import get_db, close_db
from flaskr.database.database_functions import get_general_user_statistics, get_general_movie_list



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
    db = get_db(); cur = db.cursor()

    cur.execute( f"SELECT * FROM all_users WHERE id = '{userID}';" )
    this_user = cur.fetchone()

    cur.execute( f"SELECT * FROM movies_list_info WHERE owner_id = '{userID}';" )
    user_lists = cur.fetchall()

    cur.close(); db.close()
    close_db()


    # get general list for stats
    # ---------------------------
    general_lists       = get_general_user_statistics([ this_user[0] ])
    general_list        = general_lists[this_user[0]]
    plan_to_watch       = general_list[10]   
    currently_watching  = (general_list[9] - (general_list[10] + general_list[11]))
    finished            = general_list[11]  

    # prepare stats
    # --------------
    statistics = [  ("Joined:",             str(this_user[4])[:10]  ),
                    ("Movies Completed:",   finished                ), 
                    ("Currently Watching:", currently_watching      ), 
                    ("Plan to Watch:",      plan_to_watch           ),
                    ("Watch Time:",         "24d 05h 22m"           )   ]



    # -------------------------------------------------------------------------------
    # area for the comparison code
    # -------------------------------------------------------------------------------

    '''
    statistics comparison notes:
    -----------------------------
    (just ideas, dont have to do exacly this)

        if not signed in:
            return "sign in to compare your watch histories!"

        if signed in:
            num movies in common
            num movies youve seen that they havent
            num movies theyve seen that you havent
            % match, out of total unique movies between the two of you, % that u both have seen

        if movies in common >= 6:
            top 3 closest agreement in rating + their raitng + your rating 
            top 3 biggest disagreement in rating + their raitng + your rating 
    
    '''

    # checks if the current user is logged in
    if g.user != None:
        # look in database/database_functions.py for more info on what this gives
        movie_lists = get_general_movie_list([userID, g.user[0]])



    # prepare the user comparison data for the page
    user_comparison = [ ("Similar Movies",      10),
                        ("Different Movies",    10) ]


    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------


    # return the template with all of the information we assembled for display
    return render_template('user_page/user_page.html', this_user=this_user, user_lists=user_lists, statistics=statistics, user_comparison=user_comparison)





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



