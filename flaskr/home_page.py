from flask import Flask, render_template, g, request, flash
from flaskr.db import get_database_connection
from flaskr.db import get_db
from flaskr.movieDBapi import api_home



#@app.route('/home_page/<userID>', methods=('GET', 'POST'))
def home_page(userID):

    BASE_URL    = "http://image.tmdb.org/t/p/"
    POSTER_SIZE = "w500"
    trending = api_home()["results"][:3]
    movieDisplay = []
    for movie in trending:
        temp = {

            "title"         : movie["title"],
            "poster"        : BASE_URL + POSTER_SIZE + movie["poster_path"],
        }
        movieDisplay.append(temp)
    return render_template('home_page/home_page.html', movieDisplay = movieDisplay)

    return

'''      "adult":false,
         "backdrop_path":"/mqsPyyeDCBAghXyjbw4TfEYwljw.jpg",
         "id":49046,
         "title":"All Quiet on the Western Front",
         "original_language":"de",
         "original_title":"Im Westen nichts Neues",
         "overview":"Paul Baumer and his friends Albert and Muller, egged on by romantic dreams of heroism, voluntarily enlist in the German army. Full of excitement and patriotic fervour, the boys enthusiastically march into a war they believe in. But once on the Western Front, they discover the soul-destroying horror of World War I.",
         "poster_path":"/glZfjVEzZCJ7oTHWa3m6KefcoRN.jpg",
         "media_type":"movie",
         "genre_ids":[
            28,
            18,
            36,
            10752
         ],
         "popularity":160.416,
         "release_date":"2022-10-07",
         "video":false,
         "vote_average":8.145,
         "vote_count":190
      } '''

# def api_home():
#     base        = "https://api.themoviedb.org/3"
#     api_key     = "api_key=f059b4ab8738e8777362529e74ffb62a"
#     api_url     = base + "/discover/movie?sort_by=popularity.desc&" + api_key
#     img_url     = 'https://image.tmdb.org/t/p/w500'





