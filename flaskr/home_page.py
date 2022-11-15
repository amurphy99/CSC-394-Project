from flask import Flask, render_template, g, request, flash, url_for
from flaskr.db import get_db
from flaskr.movieDBapi import trending_movies, filtered_search,api_movie_page
from flaskr.database.database_functions import get_friends_list, get_friend_requests, resolve_friend_request


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


def modal_form_resolve_request():
    sender_id   = int(request.form["sender_id"])
    receiver_id = int(request.form["receiver_id"])
    answer      = int(request.form["answer"])

    resolve_friend_request(sender_id, receiver_id, answer)

    return ""



