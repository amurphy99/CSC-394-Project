import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# REGISTER
# ----------
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                cur = db.cursor()
                cur.execute(
                    #f"INSERT INTO test_user (username, password) VALUES ({username}, {generate_password_hash(password)})"
                    # removed password hash bc caused error
                    f"INSERT INTO all_users (username, password) VALUES ('{username}', '{password}')"
                )
                db.commit()
                cur.close()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# LOGIN
# -------
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        cur = db.cursor()
        cur.execute( f"SELECT * FROM all_users WHERE username = '{username}'" )
        user = cur.fetchone()
        cur.close()

        if user is None:
            error = 'Incorrect username.'
        #elif not check_password_hash(user['password'], password):
        #elif not user['password'] == password:
        elif not user[2] == password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            #return redirect(url_for('index'))
            #return redirect( url_for('user_page', userID=user[0]) )
            return redirect( url_for('home_page') )

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cur = get_db().cursor()
        cur.execute( f"SELECT * FROM all_users WHERE id = '{user_id}'" )
        g.user = cur.fetchone()
        cur.close()

# LOGOUT
# -------
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_page'))

# Require Authentication in Other Views
# ---------------------------------------
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view