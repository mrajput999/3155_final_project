from database import db
import datetime


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    events = db.relationship("Event", backref="user", lazy=True)
    rsvp = db.relationship("Rsvp", backref="user", lazy=True)
    like = db.relationship("Like", backref="user", lazy=True)

    '''
    fav_events
    id
    '''

    def __init__(self, first_name, last_name, email, password):
        self.password = password
        self.last_name = last_name
        self.first_name = first_name
        self.email = email


class Event(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(100))
    description = db.Column(db.VARCHAR, nullable=False)
    views = db.Column("views", db.Integer())
    date = db.Column("date", db.String(100))
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rsvp = db.relationship("Rsvp", backref="event",
                           cascade='all, delete-orphan', lazy=True)
    like = db.relationship("Like", backref="event",
                           cascade='all, delete-orphan', lazy=True)

    def __init__(self, title, description, date, userId):
        self.title = title
        self.description = description
        self.date = date
        self.userId = userId
        self.views = 0


class Rsvp(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    eventId = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    def __init__(self, userId, eventId):
        self.userId = userId
        self.eventId = eventId


class Like(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    eventId = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    def __init__(self, userId, eventId):
        self.userId = userId
        self.eventId = eventId


class FavoriteEvent(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    eventId = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    def __init__(self, userId, eventId):
        self.userId = userId
        self.eventId = eventId


class EventCounter(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    count = db.Column("count", db.Integer())
