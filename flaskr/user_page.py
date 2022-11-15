from flask import Flask, render_template, g, request, flash, session, url_for

from flaskr.db import get_db, close_db
from flaskr.database.database_functions import get_general_user_statistics, get_general_movie_list, get_relationship, send_friend_request, get_friends_list, update_bio, remove_friend

from flaskr.card_display_controls import watch_list_card

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

    cur.close()#; db.close()
    


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




    # add friend button
    # ------------------
    user1        = -1
    relationship = -1
    if g.user != None:
        user1 = g.user[0]
        relationship = get_relationship(user1, userID)

    friends_button = get_friends_button(user1, userID, relationship)



    page_info = {   "num_friends"   : len(get_friends_list(userID)),
                    "user_bio"      : user_bio }

    # return the template with all of the information we assembled for display
    return render_template( 'user_page/user_page.html', 
                            this_user       = this_user,
                            page_info       = page_info, 
                            user_bio        = user_bio,
                            user_lists      = user_lists, 
                            statistics      = statistics, 
                            user_comparison = user_comparison,
                            friends_button  = friends_button       )













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








def modal_form_edit_bio():
    # get current bio
    current_bio = str(request.form["current_bio"])

    # form controls
    form_control = {    "hx-post-url"   : url_for("modal_form_edit_bio_receive"),
                        "hx-target-id"  : "#modal-body"                             }
    
    # form header
    form_header = "Edit Bio"

    # form content
    form_content = f"<input type='text' name='new_bio' value='{current_bio}'>"

    return render_template( "card_displays/modal_base.html", 
                            form_control    = form_control, 
                            form_header     = form_header,
                            form_content    = form_content      )



def modal_form_edit_bio_receive():
    if g.user == None: return "<p> sign-in error </p>"

    new_bio = str(request.form["new_bio"])
    update_bio(new_bio, g.user[0])

    return f""" <h3> New Bio:  </h3>
                <p>  {new_bio} </p>
                <script>            
                    document.getElementById("user_bio_box").innerHTML = "{new_bio}";
                </script>
                """






def friend_request_button():
    relationship = int(request.form["relationship"])
    user1        = int(request.form["user1"])
    user2        = int(request.form["user2"])

    if relationship == 0:
        send_friend_request(user1, user2)
        relationship = 2

    elif relationship == 3:
        send_friend_request(user1, user2)
        relationship = 1

    elif relationship == 1:
        remove_friend(user1, user2)
        relationship = 0

    return get_friends_button(user1, user2, relationship)



def get_friends_button(user1, user2, relationship):
    # -1 = not signed in
    #  0 = not friends, no requests
    #  1 = friends
    #  2 = outgoing friend request
    #  3 = incoming friend request

    if relationship == -1: 
        button_text = "Sign in to add friends!"
        disabled = "disabled"

    elif relationship == 0: 
        button_text = "Add Friend"
        disabled = ""

    elif relationship == 1: 
        button_text = "Remove Friend"
        disabled = ""

    elif relationship == 2: 
        button_text = "Friend Request Sent"
        disabled = "disabled"

    elif relationship == 3: 
        button_text = "Accept Incoming Friend Request"
        disabled = ""

    else:
        button_text = "problem"
        disabled = "disabled"


    button_html = f"""
        <form   id="add-friend"
                hx-post="{ url_for('friend_request_button') }"
                hx-target="#add-friend"
                hx-swap="innerHTML"
            >
            <input type="hidden" name="relationship"    value="{ relationship }">
            <input type="hidden" name="user1"           value="{ user1 }">
            <input type="hidden" name="user2"           value="{ user2 }">

            <button type="submit" { disabled }> { button_text } </button>
        </form>
        """
    return button_html





def modal_form_create_watch_list():
    # form controls
    form_control = {    "hx-post-url"   : url_for('modal_form_create_watch_list_receive') ,
                        "hx-target-id"  : "#modal-body"                             }
    
    # form header
    form_header = "Create New Watch List "

    # form content
    form_content = f"""
                    <div id="create-new-list-form">

                        <label for="new-list-title"> Title: </label>
                        <input type="text" id="new-list-title" name="new-list-title" required>

                        <label for="new-list-description"> Description: </label>
                        <input type="text" id="new-list-description" name="new-list-description"  required>

                        <input type="hidden" name="userID" value="{ g.user[0] }">

                    </div>
                    """

    return render_template( "card_displays/modal_base.html", 
                            form_control    = form_control, 
                            form_header     = form_header,
                            form_content    = form_content      )



def modal_form_create_watch_list_receive():
    if g.user == None: return "<p> sign-in error </p>"

    # get new data
    new_title   = str(request.form["new-list-title"])
    new_desc    = str(request.form["new-list-description"])
    userID      = int(request.form["userID"])

    db = get_db(); cur = db.cursor()

    cur.execute( f"INSERT INTO movies_list_info (owner_id, list_name, list_description) VALUES ({userID}, '{new_title}', '{new_desc}') RETURNING *;" )
    db.commit()
    new_list = cur.fetchone()
    
    cur.close()#; db.close()

    temp = watch_list_card(new_list[0])
    print(temp)

    # also include js in the return to insert the new watch list into the watch list div
    return f""" {temp} """















