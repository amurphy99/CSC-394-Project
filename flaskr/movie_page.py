from flask import Flask, render_template, g, request, flash
from flaskr.db import get_db
from flaskr.movieDBapi import api_home



#@app.route('/home_page/<userID>', methods=('GET', 'POST'))
def movie_page(movieID):
    
    return render_template('home_page/movie_page.html', movieID = movieID)



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