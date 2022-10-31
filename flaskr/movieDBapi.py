
import requests
#import pandas as pd
import json

from flask import Flask, render_template, g, request, flash


'''

page only shows 5 responses for now, doesnt live search, only on button click



Configuration information for poster sizes:
https://developers.themoviedb.org/3/configuration/get-api-configuration

'''

def api_query(query):
    # build api request url
    base        = "https://api.themoviedb.org/3/search/movie?api_key="
    api_key     = "f059b4ab8738e8777362529e74ffb62a"
    lang        = "&language=en-US&query="
    optionals   = "&page=1&include_adult=false"

    endpoint = base + api_key + lang + query + optionals

    # returns a dictionary
    first_response  = requests.get(endpoint)
    response_list   = first_response.json()

    print(f'query of "{query}" sent to the api')

    return response_list



#@app.route('/api_testing', methods=('GET', 'POST'))
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

 




def api_home():
    # build api request url

    base = "https://api.themoviedb.org/3/trending"
    optionals = "/movie/day?api_key="
    api_key     = "f059b4ab8738e8777362529e74ffb62a"

    endpoint = base + optionals + api_key

    # returns a dictionary
    first_response  = requests.get(endpoint)
    response_list   = first_response.json()

    print(response_list)

    return response_list