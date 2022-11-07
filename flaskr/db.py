import psycopg2
import sqlite3

import click
from flask import current_app, g


# Returns object for the database
# (need to change from hardcoded to environment variables for security)
def get_database_connection():
    conn = psycopg2.connect(
        host        = "db-hw3.cjthe8fzvkmu.us-east-1.rds.amazonaws.com",
        database    = "postgres", 
        user        = "postgres",
        password    = "Postgres*hw3" 
    )
    return conn


def get_db():
    if 'db' not in g: 

        # if in testing mode, use sqlite
        if current_app.config["TESTING"]:
            g.db = sqlite3.connect( current_app.config['DATABASE'], 
                                    detect_types=sqlite3.PARSE_DECLTYPES )
            g.db.row_factory = sqlite3.Row

        # if not in testing mode then use the actual postgres
        else: g.db = get_database_connection()

    return g.db





def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()






# schema
# ----------------------------
def init_schema():
    db  = get_db(); cur = db.cursor()

    with current_app.open_resource('database/schema.sql') as f:
        cur.execute( f.read().decode('utf8') )

    db.commit(); cur.close()

# triggers
# ----------------------------
def init_triggers():
    db  = get_db(); cur = db.cursor()

    with current_app.open_resource('database/triggers.sql') as f:
        cur.execute( f.read().decode('utf8') )

    db.commit(); cur.close()


# sample data
# ----------------------------
def init_sample_data():
    db  = get_db(); cur = db.cursor()

    with current_app.open_resource('database/sample_data.sql') as f:
        cur.execute( f.read().decode('utf8') )

    db.commit(); cur.close()






# modified command from the flask tutorial
# --------------------------------
def init_db():
    '''
    Takes 3 steps because you can't add triggers before the schema 
    is defined and you don't want to add data until the triggers 
    are defined.
    '''
    # dont do anything if testing
    if current_app.config["TESTING"]: print("init_db() called")
    else:
        init_schema()
        init_triggers()
        init_sample_data()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')





def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

















