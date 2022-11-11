
from flask import Flask, render_template, g, request, flash

from flaskr.db import get_db

from flaskr.movieDBapi import api_query, genre_query
from flaskr.database.database_functions import get_watch_list_statistics, get_poster
from flaskr.user_page import format_time

def watch_list_card(list_id):
    '''
        0 id                SERIAL
        3 list_name         TEXT
        4 list_description  TEXT
        5 recently_added    INTEGER
        7 last_updated      TIMESTAMP
        8 average_rating    NUMERIC(10,2)
        9 total_movies      INTEGER

        2 total_runtime     INTEGER
    '''
    list_statistics = get_watch_list_statistics(list_id)

    if list_statistics[0][5] == None:
        poster_path = "http://www.theprintworks.com/wp-content/themes/psBella/assets/img/film-poster-placeholder.png"
    else:
        BASE_URL    = "http://image.tmdb.org/t/p/"
        POSTER_SIZE = "w154"
        poster_path = BASE_URL + POSTER_SIZE + get_poster(list_statistics[0][5])

    formatted_runtime = format_time(list_statistics[1][2])
    
    card_info = {   "id"                : list_statistics[0][0],
                    "list_name"         : list_statistics[0][3],
                    "list_description"  : list_statistics[0][4],
                    "recently_added"    : poster_path,
                    "last_updated"      : str(list_statistics[0][7])[:10],
                    "average_rating"    : list_statistics[0][8],
                    "total_movies"      : list_statistics[0][9],
                    "total_runtime"     : formatted_runtime }

    return render_template("card_displays/watch_list_card.html", card_info=card_info)