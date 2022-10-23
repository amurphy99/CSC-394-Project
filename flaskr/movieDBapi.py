

import requests
#import pandas as pd
import json

from flask import Flask, render_template, g, request, flash


'''
page only shows 5 responses for now, doesnt live search, only on button click




api = "api_key=feb6f0eeaa0a72662967d77079850353"
endpoint = "https://api.themoviedb.org/3/search/movie?query=${search}${api}"
poster = "https://image.tmdb.org/t/p/w600/"


first_response = requests.get(base_url+facts)
response_list=first_response.json()

'''

def api_query(query):

    # api url
    base        = "https://api.themoviedb.org/3/search/movie?api_key="
    api_key     = "f059b4ab8738e8777362529e74ffb62a"
    lang        = "&language=en-US&query="
    #query       = "test"
    optionals   = "&page=1&include_adult=false"

    endpoint = base + api_key + lang + query + optionals

    # returns a dictionary
    first_response  = requests.get(endpoint)
    response_list   = first_response.json()

    print(f'query of "{query}" sent to the api')
    print(response_list)

    return response_list


#@app.route('/index', methods=('GET', 'POST'))
def api_testing():


    return render_template('api_testing/api_testing.html')


#@app.route('/send_query_htmx', methods=('GET', 'POST'))
def get_results():

    if request.method == 'POST':
        query = request.form["api_query"]
        
        results = api_query(query)
        
        first_movie = results["results"][0]

        results_tuples = []
        for key in first_movie.keys():
            temp = [key, first_movie[key]]
            results_tuples.append(temp)

        return render_template('api_testing/results_table_htmx.html', results = results_tuples)


    return "<h1> this shouldnt be returned </h1>"