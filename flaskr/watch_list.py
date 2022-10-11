from flask import Flask, render_template, g, request, flash
from flaskr.db import get_database_connection
from flaskr.db import get_db



#@app.route('/watch_list', methods=('GET', 'POST'))
def watch_list():
    list_title = "list title"
    list_owner = "list owner"
    #           ranking, title, watched?, rating
    movie_list=[["1", "Spongebob", "Completed", "10/10"],
                ["2", "Spongebob", "Completed", "10/10"],
                ["3", "Spongebob", "Completed", "10/10"],
                ["4", "Spongebob", "Completed", "10/10"],
                ["5", "Spongebob", "Completed", "10/10"],
    ]


    return render_template('watch_list/watch_list.html', list_title=list_title, list_owner=list_owner, movie_list=movie_list)




