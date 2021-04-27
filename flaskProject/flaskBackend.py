# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Like as Like
from models import User as User
from models import Rsvp as Rsvp
from models import EventCounter as eventCounter
from models import Event as Event
from models import FavoriteEvent as FavoriteEvent
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
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_user = User(first_name, last_name,
                        request.form['email'], h_password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = first_name
        session['user_id'] = new_user.id
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/home')  # Home page
def getHome():
    if session.get("user"):
        events = db.session.query(Event).all()
        event_res = []
        for event in events:
            event.likes = len(db.session.query(
                Like).filter_by(eventId=event.id).all())
            event.likeUserId = db.session.query(Like).filter_by(
                eventId=event.id, userId=session['user_id']).first()
            if db.session.query(FavoriteEvent).filter_by(eventId=event.id, userId=session["user_id"]).first():
                event.isFavorited = True
            else:
                event.isFavorited = False
            if event.likeUserId:
                event.likeUserId = event.likeUserId.id
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


@app.route("/edit-event/<eventId>", methods=["POST", "GET"])  # Edit Page
def editEvent(eventId):
    if session.get("user"):
        event = db.session.query(Event).filter_by(
            id=eventId).first()
        if request.method == "POST":
            title = request.form["title"]
            description = request.form["description"]
            date = request.form["date"]
            event.title = title
            event.description = description
            event.date = date
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('getHome'))
        else:
            if event.userId == session["user_id"]:
                if not event.date:
                    event.date = ""
                if not event.title:
                    event.title = ""
                if not event.description:
                    event.description = ""
                return render_template('newEvent.html', event=event, user=session['user'], user_id=session["user_id"])
            else:
                return redirect(url_for('getHome'))
    else:
        return redirect(url_for("login"))


@app.route("/event/delete/<eventId>")  # Delete event
def deleteEvent(eventId):
    if session.get("user"):
        event = db.session.query(Event).filter_by(id=eventId).first()
        if event.userId == session["user_id"]:
            db.session.delete(event)
            db.session.commit()
        return redirect(url_for("getHome"))
    else:
        return redirect(url_for("login"))


def getAttendess(eventId):
    rsvps = db.session.query(Rsvp).filter_by(eventId=eventId).all()
    attendess = []
    for rsvp in rsvps:
        userId = rsvp.userId
        user = db.session.query(User).filter_by(id=userId).first()
        attendess.append(user)
    return attendess


@app.route("/event/<eventId>")  # Event Page
def event(eventId):
    if session.get("user"):
        event = db.session.query(Event).filter_by(
            id=eventId).first()
        event.views += 1
        db.session.add(event)
        db.session.commit()
        rsvp = db.session.query(Rsvp).filter_by(eventId=eventId).all()
        users = []
        containsUser = False
        rsvpId = None
        for i in rsvp:
            users.append(db.session.query(User).filter_by(id=i.userId).first())
            if session["user_id"] == i.userId:
                rsvpId = i.id
                containsUser = True

        return render_template('event.html',
                               user_id=session["user_id"],
                               user=session["user"],
                               event=event,
                               attendees=users,
                               contains=containsUser,
                               rsvpId=rsvpId)
    else:
        return redirect(url_for('login'))


@app.route("/logout")  # logout page
def logout():
    if session.get("user"):
        session.clear()
    return redirect(url_for('index'))


@app.route("/rsvp/<eventId>", methods=["POST"])
def rsvp(eventId):
    if session.get("user"):
        isUser = db.session.query(Rsvp).filter_by(
            userId=session['user_id']).first()
        if not isUser:
            rsvp = Rsvp(session['user_id'], eventId)
            db.session.add(rsvp)
            db.session.commit()
        return redirect(url_for('event', eventId=eventId))
    else:
        return redirect(url_for('index'))


@app.route("/unrsvp/<rsvpId>", methods=["POST"])
def unrsvp(rsvpId):
    if session.get("user"):
        rsvp = db.session.query(Rsvp).filter_by(id=rsvpId).first()
        print(rsvp)
        if rsvp:
            eventId = rsvp.eventId
            db.session.delete(rsvp)
            db.session.commit()
            return redirect(url_for('event', eventId=eventId))
        return redirect(url_for('getHome'))

    else:
        return redirect_url('login')


@app.route("/search", methods=["POST"])
def search():

    if session.get('user'):
        term = request.form['search']
        events = db.session.query(Event).filter(Event.title.contains(term))
        return render_template("home.html", user=session['user'], user_id=session['user_id'], events=events)
    else:
        return redirect(url_for('login'))


@app.route('/event/like/<eventId>')
def like(eventId):
    if session.get("user"):
        like = Like(session["user_id"], eventId)
        db.session.add(like)
        db.session.commit()
        return redirect(url_for('getHome'))
    else:
        return redirect(url_for('login'))


@app.route('/event/dislike/<likeId>')
def dislike(likeId):
    if session.get("user"):
        like = db.session.query(Like).filter_by(id=likeId).first()
        db.session.delete(like)
        db.session.commit()
        return redirect(url_for('getHome'))
    else:
        return redirect(url_for('login'))


@app.route("/events/favorites/")
def favoriteEvents():
    if session.get("user"):
        favorites = db.session.query(FavoriteEvent).filter_by(
            userId=session['user_id']).all()
        favEvents = []
        for favorite in favorites:
            event = db.session.query(
                Event).filter_by(id=favorite.eventId).all()
            event.likes = len(db.session.query(
                Like).filter_by(eventId=event.id).all())
        return render_template('favorites.html', userId=session["user_id"], user=session['user'], events=favEvents)
    else:
        return redirect(url_for('index'))


@app.route("/favorite/<eventId>")
def favorite(eventId):
    if session.get("user"):
        if not db.session.query(FavoriteEvent).filter_by(eventId=eventId, userId=session["user_id"]).first():
            fav = FavoriteEvent(session["user_id"], eventId)
            db.session.add(fav)
            db.session.commmit()
    else:
        return redirect(url_for("index"))


@app.route("/unfavorite/<eventId>")
def unfavorite(eventId):
    if session.get("user"):
        fav = db.session.query(FavoriteEvent).filter_by(
            eventId=eventId, userId=session["user_id"]).first()
        if fav:
            db.session.delete(fav)
            db.session.commmit()
    else:
        return redirect(url_for("index"))


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(
    os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
