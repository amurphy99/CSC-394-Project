from flask import Flask, render_template, g, request, flash
from flaskr.db import get_database_connection
from flaskr.db import get_db



#@app.route('/home_page/<userID>', methods=('GET', 'POST'))
def home_page(userID):


    return render_template('home_page/home_page.html')

    return


