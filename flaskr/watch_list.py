#from lib2to3.pgen2.token import NUMBER
from flask import Flask, render_template, g, request, flash

from flaskr.db import get_database_connection
from flaskr.db import get_db

from flaskr.movieDBapi import api_query



#@app.route('/watch_list/<listID>', methods=('GET', 'POST'))
def watch_list(listID):
    '''
    Sends:
        listID
            * listID that was received in function call
        
        list_info
            * database entry from movies_list_info for the given listID
        
        owner_username
            * username of the owner of the listID received
        
        display_list
            * list of dictionaries with the following:
                - id
                - status
                - rating
                - title
                - source
                - popularity

    '''
    # constants for building poster path
    BASE_URL    = "http://image.tmdb.org/t/p/"
    POSTER_SIZE = "w154"
    # prepare variables to send to template
    display_list = []

    # retrieve all data required
    db = get_db(); cur = db.cursor()

    cur.execute( f"SELECT * FROM movies_list_info WHERE id = '{listID}';" )
    list_info = cur.fetchone()

    cur.execute( f"SELECT * FROM test_user WHERE id = '{list_info[1]}';" )
    list_owner = cur.fetchone()

    cur.execute( f"SELECT * FROM movies_list WHERE list_id = '{list_info[0]}';" )
    movie_list = cur.fetchall()

    # organize data for the display_list that will be sent to the page template
    for movie in movie_list:
        cur.execute( f"SELECT * FROM movies WHERE id = '{movie[0]}';" )
        movie_info = cur.fetchone()

        if      movie[2] == 0:  str_watch_status = "Plan to Watch" 
        elif    movie[2] == 1:  str_watch_status = "Currently Watching"
        elif    movie[2] == 2:  str_watch_status = "Finished Watching"
        else:                   str_watch_status = "(watch status not entered)"

        movie_display = {   "id"            : movie[0],
                            "status"        : str_watch_status,
                            "rating"        : movie[3],
                            "title"         : movie_info[1],
                            "poster"        : BASE_URL + POSTER_SIZE + movie_info[2],
                            "popularity"    : movie_info[3]     }

        display_list.append(movie_display)

    cur.close(); db.close()


    return render_template('watch_list/watch_list.html', list_info=list_info, owner_username=list_owner[1], movies_list=display_list, listID=listID)




# app.add_url_rule('/watch_list/modal', methods=('GET', 'POST'), view_func=watch_list.add_movie_modal)
def add_movie_modal():
    # safeguard
    if request.method != 'POST': return "<h1> non-POST request to 'get_move_cards()' </h1>"

    listID = int(request.form["listID"])

    return render_template('watch_list/add_movie_modal.html', listID=listID)




# app.add_url_rule('/watch_list/get_movie_cards', methods=('GET', 'POST'), view_func=watch_list.get_movie_cards)
def get_movie_cards():
    # safeguard
    if request.method != 'POST': return "<h1> non-POST request to 'get_move_cards()' </h1>"

    # get request info
    listID      = int(request.form["listID"])
    query       = request.form["api_query"]
    if len(query) < 1: return 

    # for api request feedback
    api_results = api_query(query)
    total_results = api_results["total_results"]

    # only showing 3 results for now while testing
    INFO            = ["title", "id", "overview", "release_date"]
    NUMBER_SHOWN    = 3
    if total_results < NUMBER_SHOWN: NUMBER_SHOWN = total_results
        
    results = []
    for i in range(NUMBER_SHOWN):
        single_movie = api_results["results"][i]
        
        movie_info = {}
        # image -> dict{image source, alt text}
        BASE_URL    = "http://image.tmdb.org/t/p/"
        POSTER_SIZE = "w92"
        image_source = single_movie["poster_path"]
        movie_info["source"] = BASE_URL + POSTER_SIZE + image_source 

        alt_text = "Poster for: " + single_movie["title"]
        movie_info["alt_text"]   = alt_text

        # info  -> list of tuples (key, value)
        results_tuples = []
        for key in INFO:
            results_tuples.append( (key, single_movie[key]) )
        movie_info["info"] = results_tuples

        # append this movies info
        results.append(movie_info)

    return render_template('watch_list/get_movie_cards_htmx.html', results = results, api_feedback = (NUMBER_SHOWN, total_results), listID=listID)




# app.add_url_rule('/watch_list/show_user_input_form', methods=('GET', 'POST'), view_func=watch_list.show_user_input_form)
def show_user_input_form():
    '''
    Receiving:
        movie info

    '''
    # create the new watch list
    if request.method == 'POST':
        movie   = eval(request.form["movie_info"])
        listID  = int (request.form["listID"    ])
  
        return render_template('watch_list/add_movie_user_inputs_htmx.html', movie=movie, listID=listID)

    return 



# app.add_url_rule('/watch_list/movie_added_htmx', methods=('GET', 'POST'), view_func=watch_list.movie_added)
def movie_added():
    '''
    Receiving:
        * movie info
        * userID (can use to make sure the user has permissions to modify this list)
        * completion status
        * rating

    Sending:
        * movie info
        * watch_status
            0 = Plan to Watch 
            1 = Currently Watching
            2 = Finished Watching
        * rating

    cant do the add/update table syntax how i would like in python:
    ----------------------------------------------------------------
    cur.execute(f"
        IF NOT EXISTS ( SELECT * FROM movies WHERE id = '{f_movie_id}' )
            /* insert */
            INSERT INTO movies (id, title, poster) VALUES ('{f_movie_id}', '{f_movie_title}', '{f_movie_source}');
        ELSE
            /* update */
            UPDATE movies SET popularity = popularity + 1 WHERE id = '{f_movie_id}';
    ")
    
    '''
    # create the new watch list
    if request.method == 'POST':
        # get form data
        movie           = eval(request.form["movie_info"    ])
        listID          = int (request.form["listID"        ])
        userID          = int (request.form["userID"        ])
        watch_status    = int (request.form["watch-status"  ])
        rating          = int (request.form["rating"        ])

        # prepare sql statements
        f_movie_id      = movie["info"][1][1]
        f_movie_title   = movie["info"][0][1]
        f_movie_source  = movie["source"]

        db = get_db(); cur = db.cursor()

        # first add/update the movie table
        cur.execute( f"INSERT INTO movies (id, title, poster) VALUES ('{f_movie_id}', '{f_movie_title}', '{f_movie_source}') ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;" )
        db.commit()

        # add to movies_list table
        cur.execute(f"INSERT INTO movies_list (movie_id, list_id, status, rating) VALUES ('{f_movie_id}', '{listID}', '{watch_status}', '{rating}')")
        db.commit()
        
        cur.close(); db.close()

        # convert watch status into a string
        str_watch_status = ""
        if      watch_status == 0:  str_watch_status = "Plan to Watch" 
        elif    watch_status == 1:  str_watch_status = "Currently Watching"
        elif    watch_status == 2:  str_watch_status = "Finished Watching"
        else:                       str_watch_status = "(watch status not entered)"

        # return a template with the movie card and users inputs
        return render_template('watch_list/movie_added_htmx.html', movie=movie, watch_status=str_watch_status, rating=rating)

    return "<h1> this should not return </h1>"

