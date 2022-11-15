from flask import Flask, render_template, g, request, flash, session, url_for

from flaskr.db import get_db, close_db
from flaskr.database.database_functions import get_general_user_statistics, get_general_movie_list

def format_time(time):
    days    = int(time // (24*60))
    hours   = int((time-(days*24)) // 60)
    minutes = int(time-((days*24*60)+(hours*60)))

    formatted_time = ""
    if days > 0: 
        formatted_time += f"{days:2}d "
        formatted_time += f"{hours:2}h "
        formatted_time += f"{minutes:2}m"
        return formatted_time

    elif hours > 0:
        formatted_time += f"{hours:2}h "
        formatted_time += f"{minutes:2}m"
        return formatted_time

    else:
        formatted_time += f"{minutes:2}m"
        return formatted_time




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
    general_lists           = get_general_user_statistics([ this_user[0] ])
    general_list_info       = general_lists[this_user[0]][0]
    general_list_statistics = general_lists[this_user[0]][1]

    plan_to_watch       = general_list_info[10]   
    currently_watching  = (general_list_info[9] - (general_list_info[10] + general_list_info[11]))
    finished            = general_list_info[11]  
    user_bio            = general_list_info[4]
    total_movies        = int(general_list_statistics[1])
    total_watch_time    = format_time(general_list_statistics[2])
    total_budget        = f"${general_list_statistics[3]:,}"

    if total_movies == 0:
        average_watch_time  = "--"
        average_budget      = "--"
    else:
        average_watch_time  = format_time((round((general_list_statistics[2]/total_movies),2)))
        average_budget      = f"${round((general_list_statistics[3]/total_movies),2):,}"

    # prepare stats
    # --------------
    statistics = [  ("Joined:",             str(this_user[4])[:10]  ),
                    ("Total Movies Added:", total_movies            ),
                    ("Total Runtime:",      total_watch_time        ), 
                    ("Average Runtime:",    average_watch_time      ),
                    ("Total Budget:",       total_budget            ), 
                    ("Average Budget:",     average_budget          ),  
                    ("Movies Completed:",   finished                ), 
                    ("Currently Watching:", currently_watching      ), 
                    ("Plan to Watch:",      plan_to_watch           )   ] 



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
    return render_template( 'user_page/user_page.html', 
                            this_user       = this_user, 
                            user_bio        = user_bio,
                            user_lists      = user_lists, 
                            statistics      = statistics, 
                            user_comparison = user_comparison   )




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








def test_modal():

    if request.method == 'POST':
        info = str(request.form["info"])

        return render_template("card_displays/modal_base.html", test_body_content=info) 

    return "<h1> shouldnt be returned </h1>"




def test_modal_receive():

    if request.method == 'POST':
        info = str(request.form["info"])
        print(info)

        return "empty"

    return "<h1> shouldnt be returned </h1>"







def modal_form_edit_bio():
    # form controls
    form_control = {    "hx-post-url"   : url_for("modal_form_edit_bio_receive"),
                        "hx-target-id"  : "#modal-body"                             }

    # form header
    form_header = "Edit Bio"

    # form content
    form_content = "<input type='text' name='new_bio' value='previous bio'>"

    print(render_template( "card_displays/modal_base.html", 
                            form_control    = form_control, 
                            form_header     = form_header,
                            form_content    = form_content      ))

    return render_template( "card_displays/modal_base.html", 
                            form_control    = form_control, 
                            form_header     = form_header,
                            form_content    = form_content      )



def modal_form_edit_bio_receive():

    info = str(request.form["new_bio"])
    print(info)

    return f"<p> {info} </p>"








