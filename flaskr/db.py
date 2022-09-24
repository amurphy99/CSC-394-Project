import psycopg2

import click
from flask import current_app, g


# Returns object for the database
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
        g.db = get_database_connection()
    
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()





def init_db():
    db  = get_db()
    cur = db.cursor()

    cur.execute('DROP TABLE IF EXISTS test_user;')
    cur.execute('CREATE TABLE test_user (id        serial  PRIMARY KEY,'
                                        'username  TEXT    UNIQUE NOT NULL,'
                                        'password  TEXT    NOT NULL);'
                                        )


    with current_app.open_resource('schema.sql') as f:
        cur.execute( f.read().decode('utf8') )
    db.commit()
    cur.close()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')





def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

















