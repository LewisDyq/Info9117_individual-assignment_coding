import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

os.environ['FLASK_APP'] = 'flaskr' # to avoid error msg
app = Flask(__name__)
os.chdir('E:\\INFO9117\\flaskr')
conn = sqlite3.connect(r'./flaskr.db')
db = conn.cursor()
sql = '''select * from users'''
results = db.execute(sql)
all_users = results.fetchall()

app.config.update(dict(
    DATEBASE=os.path.join(app.root_path,'flaskr.db'),
    SECRET_KEY='My key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
def connect_db():
    """ Connect to database """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        # if app.environment == 'test':
        #     os.unlink(app.config['DATABASE') # can't delete here


def init_db(schema='schema.sql'):
    db = get_db()
    with app.open_resource(schema, mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute("SELECT username FROM users ORDER BY username DESC")
    name = cur.fetchall()
    return render_template('show_entries.html', users=name)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session['logged_in']:
        abort(401)
    db=get_db()
    db.execute("insert into entries(title,text) values (?,?)", [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry added')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            db = get_db()
            cur = db.execute("select * from users where username =? and password = ?", [username,password])
            rows = cur.fetchone()
            if rows:
                session['logged_in'] = True
                flash("Login Success!")
            else:
                error = "Bad Login"
        else:
            error = "Missing user credentials"

    return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You have been logged out")
    return redirect(url_for('show_entries'))


def serve_forever():
    app.run()


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with Werkzeug server")
    if app.environment == 'test':
        func()
        os.unlink(app.config['DATABASE'])


@app.route('/shutdown')
def shutdown():
    if app.environment == 'test':
        shutdown_server()
    return "Server shutdown"

@app.cli.command('start')
def start():
    app.config.from_object(__name__) # load config from this file

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'flaskr.db'),
        SECRET_KEY='Production key',
    ))
    app.config.from_envvar('FLASKR_SETTINGS',  silent=True)

    app.run()


def test_server():
    ### Setup for integration testing
    app.config.from_object(__name__) # load config from this file

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'flaskr_test.db'),
        SECRET_KEY='Test key',
        SERVER_NAME='localhost:5000',
        Login_NAME='localhost/login:5000',
        # DEBUG=True, # does not work from behave
    ))
    app.environment = 'test'
    with app.app_context():
        init_db('test_schema.sql')
    app.run()

if __name__ == '__main__':
        start()