from flask import Flask, render_template, g, request, flash, url_for
from flaskr.db import get_db
from flaskr.movieDBapi import trending_movies, filtered_search,api_movie_page
from flaskr.database.database_functions import get_friends_list, get_friend_requests, resolve_friend_request, get_relationship


#@app.route('/', methods=('GET', 'POST'))
def home_page():
    '''
        later on will be using g.user to display friends list
        when g.user is None, load something else in that area
    '''
    # Poster url
    BASE_URL    = "http://image.tmdb.org/t/p/"
    POSTER_SIZE = "w500"

    trending = trending_movies()["results"][:9]
    # prepare movie data for display
    movieDisplay = []
    genre_string = ''
    for movie in trending:
        result_movie = api_movie_page(movie['id'])
        genre_list = []
        for key in result_movie['genres']:
            genre_list.append(key['name'])
        genre_string = ', '.join(genre_list)
        temp = {    "title"         : movie["title"],
                    "poster"        : BASE_URL + POSTER_SIZE + movie["poster_path"],
                    "id"            : movie["id"],
                    "overview"      : movie["overview"],
                    "release_date"  : movie["release_date"],
                    "genres"        : genre_string

                    }
        movieDisplay.append(temp)



    # prepare friends list for display [id, username]
    if g.user == None:  user_friends = []
    else:               user_friends = get_friends_list(g.user[0])


    # display page
    return render_template('home_page/home_page.html', movieDisplay=movieDisplay, user_friends=user_friends)




#/home_page/home_page_search
def home_filter_tags():
    if request.method != 'POST': return "<h1> non-POST request to 'get_move_cards()' </h1>"

    tags = request.form.getlist("myCheckbox")

    placeholder = "Searching for: "
    safe_tags   = []
    for tag in tags:
        if tag != '':
            safe_tags.append(tag)
            placeholder += str(tag) + ", "

    placeholder = placeholder[:-2] + "..."

    return render_template("home_page/filter_tags_htmx.html", tags=safe_tags, placeholder=placeholder)




def new_trending_list():
    if request.method != 'POST': return "<h1> non-POST request to 'get_move_cards()' </h1>"

    # constants:
    # -----------
    BASE_URL    = "http://image.tmdb.org/t/p/"
    POSTER_SIZE = "w500"


    # user inputs:
    # -------------
    tags    = request.form.getlist("genre-tag")
    method  = int(request.form["sort-by"])
    query   = request.form["searched"]

    # get results:
    # -------------
    results = filtered_search(tags, method, query, num_results=9)
    matches = results["matches"]

    keys = list(results.keys())
    for key in keys[1:]:
        print(f"{key} : {results[key]}")

    
    # prepare movies for display
    # ---------------------------
    movieDisplay = []
    genre_string = ''        
    for movie in matches:
        result_movie = api_movie_page(movie['id'])
        genre_list = []
        for key in result_movie['genres']:
            genre_list.append(key['name'])
        genre_string = ', '.join(genre_list)
        temp = {    "title"     : movie["title"],
                    "poster"    : BASE_URL + POSTER_SIZE + movie["poster_path"],
                    "id"        : movie["id"],
                    "overview"  : movie["overview"],
                    "release_date": movie["release_date"],
                    "genres" : genre_string
                     }
        movieDisplay.append(temp)

    # return
    return render_template('home_page/new_trending_list_htmx.html', movieDisplay = movieDisplay)




'''
def modal_form_add_friends():
    user_id = int(request.form["user_id"])
    friend_requests = get_friend_requests(user_id)

    form_control    = { "hx-post-url"   : url_for("modal_form_resolve_request"),
                        "hx-target-id"  : "#modal-body"                             }
    form_header     = "Manage Friends"
    form_content    = render_template("home_page/modal_form_add_friends.html", friend_requests=friend_requests)

    return render_template( "card_displays/modal_base.html", 
                            form_control    = form_control, 
                            form_header     = form_header,
                            form_content    = form_content      )
'''



def modal_form_add_friends():
    user_id = int(request.form["user_id"])

    friend_requests = get_friend_requests(user_id)

    form_header     = "Manage Friends"

    return render_template( "home_page/add_friends_modal.html", 
                            form_header     = form_header,
                            friend_requests = friend_requests      )


def modal_form_resolve_request():
    if "username" in request.form: return modal_form_search_users2(str(request.form["username"]))

    sender_id   = int(request.form["sender_id"])
    receiver_id = int(request.form["receiver_id"])
    answer      = int(request.form["answer"])

    resolve_friend_request(sender_id, receiver_id, answer)

    return ""


def modal_form_search_users():
    username = str(request.form["username"])
    #print(username)

    db = get_db(); cur = db.cursor()

    cur.execute(f"SELECT * FROM all_users ORDER BY SIMILARITY(username,'{username}') DESC LIMIT 3;")
    results = cur.fetchall()
    
    cur.close()
    #print(results)

    user1 = g.user[0]
    search_results = []
    for result in results:
        user_id = result[0] 
        username = result[1]
        relationship = get_relationship(user1, user_id)
        friends_button = get_friends_button(user1, user_id, relationship)

        search_results.append( [user_id, username, friends_button] )

        
    return render_template("home_page/user_search_results.html", search_results=search_results)




def get_friends_button(user1, user2, relationship):

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
        <form   id="add-friend-{user2}"
                hx-post="{ url_for('friend_request_button') }"
                hx-target="#add-friend-{user2}"
                hx-swap="innerHTML"
            >
            <input type="hidden" name="relationship"    value="{ relationship }">
            <input type="hidden" name="user1"           value="{ user1 }">
            <input type="hidden" name="user2"           value="{ user2 }">

            <button class="btn btn-primary" type="submit" { disabled }> { button_text } </button>
        </form>
        """
    return button_html
















def modal_form_search_users2(username):
    #print(username)

    db = get_db(); cur = db.cursor()

    #cur.execute(f"CREATE EXTENSION pg_trgm;")
    #db.commit()

    cur.execute(f"SELECT * FROM all_users ORDER BY SIMILARITY(username,'{username}') DESC LIMIT 3;")
    results = cur.fetchall()
    
    cur.close()
    #print(results)

    return f"<p> {username} </p>"
