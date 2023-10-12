from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"

@app.route('/')

def home():
    return render_template("home.html")

@app.route('/login')

def login():
    return render_template("login.html")

@app.route('/AboutUs')

def AboutUs(): 
    return render_template("AboutUs.html")

@app.route('/addLab')

def addLab():
    return render_template("addLab.html")

@app.route('/addSoftware')

def addSoftware():
    return render_template("addSoftware.html")

