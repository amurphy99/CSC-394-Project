
from flask import Flask, render_template, g, request, flash

from flaskr.db import get_db

from flaskr.movieDBapi import api_query
from flaskr.database.database_functions import get_watch_list_statistics, get_poster
#from flaskr.user_page import format_time


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


def movie_card(movie):
    '''
    movie = dict
        * "id"      = movieDB id
        * "title"   = movie title
        * "poster"  = url for the movies poster image

    '''
    return render_template("card_displays/movie_card.html", movie=movie)



def watch_list_movie_card(movie_info):
    '''
    Receive:
    ---------
        movie_display = {   "id"            : movie[0],
                            "status"        : str_watch_status,
                            "rating"        : movie[3],
                            "title"         : movie_info[1],
                            "poster"        : BASE_URL + POSTER_SIZE + movie_info[2],
                            "popularity"    : movie_info[3]     }
    Return:
    --------
        card_info = {   "status"    : "user watch status",
                        "rating"    : "user rating",
                        "movie"     : "dict with: id, title, poster" }
    '''

    movie = { "id": movie_info["id"], "title": movie_info["title"], "poster": movie_info["poster"] }


    card_info = {   "status"    : movie_info["status"],
                    "rating"    : movie_info["rating"],
                    "movie"     : movie }



    return render_template("card_displays/watch_list_movie_card.html", card_info=card_info)



