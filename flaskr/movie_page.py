from flask import Flask, render_template, g, request, flash
from flaskr.db import get_db
from flaskr.movieDBapi import api_home
from flaskr.movieDBapi import api_movie_page
from flaskr.movieDBapi import api_query



#@app.route('/home_page/<userID>', methods=('GET', 'POST'))
def movie_page(movieID):
    
    result_movie = api_movie_page(movieID)

    print(result_movie)

    return render_template('home_page/movie_page.html', movieID = movieID)



'''      
sample api output:
-------------------
{
   "adult":false,
   "backdrop_path":"/yzqaKAhglTrkeOfuIXYYArf0WnA.jpg",
   "belongs_to_collection":{
      "id":137697,
      "name":"Finding Nemo Collection",
      "poster_path":"/ucM59odfzLdQlmtNVAkmiB9Qw3J.jpg",
      "backdrop_path":"/2hC8HHRUvwRljYKIcQDMyMbLlxz.jpg"
   },
   "budget":94000000,
   "genres":[
      {
         "id":16,
         "name":"Animation"
      },
      {
         "id":10751,
         "name":"Family"
      }
   ],
   "homepage":"http://movies.disney.com/finding-nemo",
   "id":12,
   "imdb_id":"tt0266543",
   "original_language":"en",
   "original_title":"Finding Nemo",
   "overview":"Nemo, an adventurous young clownfish, is unexpectedly taken from his Great Barrier Reef home to a dentist's office aquarium. It's up to his worrisome father Marlin and a friendly but forgetful fish Dory to bring Nemo home -- meeting vegetarian sharks, surfer dude turtles, hypnotic jellyfish, hungry seagulls, and more along the way.",
   "popularity":144.729,
   "poster_path":"/eHuGQ10FUzK1mdOY69wF5pGgEf5.jpg",
   "production_companies":[
      {
         "id":3,
         "logo_path":"/1TjvGVDMYsj6JBxOAkUHpPEwLf7.png",
         "name":"Pixar",
         "origin_country":"US"
      }
   ],
   "production_countries":[
      {
         "iso_3166_1":"US",
         "name":"United States of America"
      }
   ],
   "release_date":"2003-05-30",
   "revenue":940335536,
   "runtime":100,
   "spoken_languages":[
      {
         "english_name":"English",
         "iso_639_1":"en",
         "name":"English"
      }
   ],
   "status":"Released",
   "tagline":"There are 3.7 trillion fish in the ocean. They're looking for one.",
   "title":"Finding Nemo",
   "video":false,
   "vote_average":7.826,
   "vote_count":16963
}
'''