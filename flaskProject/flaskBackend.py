# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template  # Import html Jimja2

app = Flask(__name__)     # create an app

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page

##		Landing Page	##


@app.route('/')
def index():
    return 'Hello World!'

##		Login Page	##


@app.route('/login')
def getLogin():
    return "Login page"


##		Register Page ##
@app.route('/register')
def getRegister():
    return "Register page"

## 	Home page	##


@app.route('/home')
def getHome():
    return "Home Page"

##		Create Event   ##


@app.route("/create-event")
def getCreate():
    return "Create Event Page"

##		Edit Page 	##


@app.route("/edit-event/<eventId>")
def getEdit():
    return "Edit Event Page"

##		Event Page		##


@app.route("/event/<eventId>")
def getEvent():
    return "get event page"


@route("/logout")
def logout():
    #Redirect to the home page#


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(
    os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
