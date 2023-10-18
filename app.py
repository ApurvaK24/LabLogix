from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField
from wtforms.validators import DataRequired
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import date
# from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm, SearchForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm
# from flask_ckeditor import CKEditor
# from werkzeug.utils import secure_filename
# import uuid as uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


@app.route('/')

def home():
    return render_template("home.html")

@app.route('/login')

def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
			# Check the hash
            if check_password_hash(user.password_hash, form.password.data):
             login_user(user)
             flash("Login Succesfull!!")
             return redirect(url_for('dashboard'))
            else:
              flash("Wrong Password - Try Again!")
        else:
          flash("That User Doesn't Exist! Try Again...")


    return render_template('login.html', form=form)
     
    # return render_template("login.html")

@app.route('/AboutUs')

def AboutUs(): 
    return render_template("AboutUs.html")

@app.route('/addLab')

def addLab():
    return render_template("addLab.html")

@app.route('/addSoftware')

def addSoftware():
    return render_template("addSoftware.html")

@app.route('/LabListing')

def LabListing():
    return render_template("LabListing.html")

@app.route('/SoftwareListing')

def SoftwareListing():
    return render_template("SoftwareListing.html")

if __name__ == "__main__":
    app.run(debug=True,port=8000)


