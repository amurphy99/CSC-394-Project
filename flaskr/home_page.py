from flask import Flask, render_template, g, request, flash
from flaskr.db import get_db
from flaskr.movieDBapi import api_home



#@app.route('/home_page/<userID>', methods=('GET', 'POST'))
def home_page(userID):
    # Poster url 
    BASE_URL    = "http://image.tmdb.org/t/p/"
    POSTER_SIZE = "w500"

    # api call to get trending movies
    trending = api_home()["results"][:9]

    # prepare movie data for display
    movieDisplay = []
    for movie in trending:
        temp = {    "title"     : movie["title"],
                    "poster"    : BASE_URL + POSTER_SIZE + movie["poster_path"] }

        movieDisplay.append(temp)

    # prepare friends list for display [id, username]
    user_friends = [    ["admin",   1], 
                        ["Andrew",  2],
                        ["Calvin",  3],
                        ["Joseph",  4],
                        ["Brenden", 5],
                        ["Derrick", 6],
                        ["Benas",   7]  ]

    # display page
    return render_template('home_page/home_page.html', movieDisplay=movieDisplay, user_friends=user_friends)



'''      
sample api output:
-------------------
    "adult":false,
    "backdrop_path":"/mqsPyyeDCBAghXyjbw4TfEYwljw.jpg",
    "id":49046,
    "title":"All Quiet on the Western Front",
    "original_language":"de",
    "original_title":"Im Westen nichts Neues",
    "overview":"Paul Baumer and his friends Albert and Muller, egged on by romantic dreams of heroism, voluntarily enlist in the German army. Full of excitement and patriotic fervour, the boys enthusiastically march into a war they believe in. But once on the Western Front, they discover the soul-destroying horror of World War I.",
    "poster_path":"/glZfjVEzZCJ7oTHWa3m6KefcoRN.jpg",
    "media_type":"movie",
    "genre_ids":[ 28, 18, 36, 10752 ],
    "popularity":160.416,
    "release_date":"2022-10-07",
    "video":false,
    "vote_average":8.145,
    "vote_count":190
'''



