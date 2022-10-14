from flask import Flask, render_template, g, request, flash
from flaskr.db import get_database_connection
from flaskr.db import get_db



#@app.route('/watch_list/<listID>', methods=('GET', 'POST'))
def watch_list(listID):

    display_list = []


    db  = get_db()
    cur = db.cursor()

    cur.execute( f"SELECT * FROM movies_list_info WHERE id = '{listID}';" )
    this_list = cur.fetchone()

    cur.execute( f"SELECT * FROM test_user WHERE id = '{this_list[1]}';" )
    list_owner = cur.fetchone()

    cur.execute( f"SELECT * FROM movies_list WHERE list_id = '{this_list[0]}';" )
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


    cur.close()
    db.close()

    list_title = this_list[4]
    list_owner = list_owner[1]


    return render_template('watch_list/watch_list.html', list_title=list_title, list_owner=list_owner, movie_list=display_list)




