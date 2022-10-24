from lib2to3.pgen2.token import NUMBER
from flask import Flask, render_template, g, request, flash
from flaskr.db import get_database_connection
from flaskr.db import get_db

from flaskr.movieDBapi import api_query



#@app.route('/watch_list/<listID>', methods=('GET', 'POST'))
def watch_list(listID):
    display_list = []


    db = get_db(); cur = db.cursor()

    cur.execute( f"SELECT * FROM movies_list_info WHERE id = '{listID}';" )
    list_info = cur.fetchone()

    cur.execute( f"SELECT * FROM test_user WHERE id = '{list_info[1]}';" )
    list_owner = cur.fetchone()

    cur.execute( f"SELECT * FROM movies_list WHERE list_id = '{list_info[0]}';" )
    movie_list = cur.fetchall()

    for movie in movie_list:
        cur.execute( f"SELECT * FROM movies WHERE id = '{movie[0]}';" )
        temp = cur.fetchone()
        if movie[2] == 0:
            display_list.append([temp[1], "Plan to watch"])
        elif movie[2] == 1:
            display_list.append([temp[1], "Currently Watching"])
        else:
            display_list.append([temp[1], "Finished"])

    cur.close(); db.close()


    owner_username = list_owner[1]

    return render_template('watch_list/watch_list.html', list_info=list_info, owner_username=owner_username, movies_list=display_list)




# app.add_url_rule('/watch_list/modal', methods=('GET', 'POST'), view_func=watch_list.add_movie_modal)
def add_movie_modal():
    return render_template('watch_list/add_movie_modal.html')



# app.add_url_rule('/watch_list/get_movie_cards', methods=('GET', 'POST'), view_func=watch_list.get_movie_cards)
def get_movie_cards():
    # safeguard
    if request.method != 'POST': return "<h1> non-POST request to 'get_move_cards()' </h1>"

    # get request info
    query   = request.form["api_query"]
    api_results = api_query(query)

    # for api request feedback
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

    print(results)

    return render_template('watch_list/get_movie_cards_htmx.html', results = results, api_feedback = (NUMBER_SHOWN, total_results))

