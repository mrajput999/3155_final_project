# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
# from models import Note as Note
from models import User as User
from models import EventCounter as eventCounter
from models import Event as Event
from forms import RegisterForm, LoginForm
from flask import session
import bcrypt
app = Flask(__name__)     # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()    # create an app

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page


@app.route('/')  # Landing Page
def index():
    c = db.session.query(eventCounter).all()
    print(c)
    if session.get("user"):
        return render_template("index.html", user=session['user'], user_id=session['user_id'], eventCount=len(c))
    else:
        return render_template("index.html", eventCount=len(c))


@app.route('/login', methods=["POST", "GET"])  # Login Page
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = db.session.query(User).filter_by(
            email=request.form['email']).one()
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), user.password):
            session['user'] = user.first_name
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            form.password.errors = ["Incorrect username or password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route('/register', methods=['POST', "GET"])  # Register Page
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name,
                        request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        # access id value from user model of this newly added user
        session['user_id'] = new_user.id
        # show user dashboard view
        return redirect(url_for('index'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


@app.route('/home')  # Home page
def getHome():
    if session.get("user"):
        events = db.session.query(Event).all()
        print(events)
        event_res = []
        for event in events:
            if not event.date:
                event.date = "date not provided"
        return render_template("home.html", user=session['user'], user_id=session['user_id'], events=events)
    else:
        return redirect(url_for('login'))


@app.route("/create-event", methods=["POST", "GET"])  # Create Event
def create_event():
    print(session.get("user"))
    if session.get("user"):
        if request.method == "POST":
            title = request.form["title"]
            description = request.form["description"]
            date = request.form["date"]
            print(title, description, date)
            if not title:
                title = "No title provided"
            if not description:
                description = "No description provided"
            if not date:
                date = None
            new_event = Event(title, description, date, session["user_id"])
            db.session.add(new_event)
            incremntCount = eventCounter()
            db.session.add(incremntCount)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template("newEvent.html", user=session["user"], user_id=session["user_id"])
    else:
        return redirect(url_for('login'))


@app.route("/edit-event/<eventId>")  # Edit Page
def getEdit():
    return "Edit Event Page"


@app.route("/event/<eventId>")  # Event Page
def getEvent():
    return "get event page"


@app.route("/logout")  # logout page
def logout():
    if session.get("user"):
        session.clear()
    return redirect(url_for('index'))
    #Redirect to the home page#


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(
    os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
