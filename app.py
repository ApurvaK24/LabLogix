# from flask import Flask, render_template
# from flask_wtf import FlaskForm
# from wtforms import StringField , SubmitField
# from wtforms.validators import DataRequired
# from datetime import datetime 
# from flask_sqlalchemy import SQLAlchemy
# # from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash 
# from datetime import date
# from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm, SearchForm
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm
# from flask_ckeditor import CKEditor
# from werkzeug.utils import secure_filename
# import uuid as uuid
from flask import Flask, flash, render_template,session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = "Shooo!This is secretkey"
# app.config['MYSQL_HOST']='sql12.freemysqlhosting.net'
# app.config['MYSQL_USER']='sql12652718'
# app.config['MYSQL_PASSWORD']='DsRaiJa9kh'
# app.config['MYSQL_DB']='sql12652718'
app.config['MYSQL_DATABASE_HOST']='sql12.freemysqlhosting.net'
app.config['MYSQL_DATABASE_USER']='sql12652718'
app.config['MYSQL_DATABASE_PASSWORD']='DsRaiJa9kh'
app.config['MYSQL_DATABASE_DB']='sql12652718'
mysql = MySQL()
mysql.init_app(app)

bcrypt = Bcrypt(app)

# Flask_Login Stuff

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(user_id):
# 	return Users.query.get(int(user_id))

# class RegisterForm(FlaskForm):
#     username = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Register')

#     def validate_username(self, username):
#         existing_user_username = User.query.filter_by(
#             username=username.data).first()
#         if existing_user_username:
#             raise ValidationError(
#                 'That username already exists. Please choose a different one.')

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    curr= mysql.connect().cursor()
    curr.execute("select * from user where id = %s", (user_id,))
    result = curr.fetchall()
    if result is not None:
        myuser=OurUser(result)
        user=User(myuser.user_id)
        curr.close()
        return user
    else:
        curr.close()
        return None
    

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    role = SelectField(u'Select Role', choices=[('Admin', 'Admin'), ('Professor', 'Professor'), ('Assistant', 'Assistant')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # pass
        curr= mysql.connect().cursor()
        curr.execute(f"select * from user where username={username}")
        result = curr.fetchall()
        myuser=OurUser(result)
        curr.close()
        
        if username==myuser.username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Username"})
    # username = StringField(validators=[
    #                        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired()],  render_kw={"placeholder": "Password"})

    role = SelectField(u'Select Role', choices=[('Admin', 'Admin'), ('Professor', 'Professor'), ('Assistant', 'Assistant')])

    submit = SubmitField('Submit')


@app.route('/')
def home():
    
    curr= mysql.connect().cursor()
    return render_template("home.html")


#sql methods-----------------------------
# curr= mysql.connect().cursor()
#     # curr.execute("create table user(id int primary key auto_increment,username varchar(100) not null, password varchar(100), role varchar(100) )")
#     curr.execute("insert into user (username,password,role) values ('atharvak','abcd','Admin')")
#     mysql.connection.commit()
#     curr.execute("show tables")
#     result = curr.fetchall()
#     print(result)
#     curr.close()
# --------------------------------------------


class OurUser :
    def __init__(self, tupp):
        try:
            self.user_id = tupp[0][0]
            self.username = tupp[0][1]
            self.password = tupp[0][2]
            self.role = tupp[0][3]
        
        except:
            self.user_id = None
            self.username = None
            self.password = None
            self.role = None
            

@app.route('/login', methods=['GET', 'POST'])
def login():
    curr= mysql.connect().cursor()
    error = None
    username=None
    
    form = LoginForm()
    if form.validate_on_submit():
        curr= mysql.connect().cursor()
        username=form.username.data
        # print("Validation button ck",username)
        # user = User.query.filter_by(username=form.username.data).first()
        curr.execute("select * from user where username='{}'".format(username))
        result = curr.fetchall()
        myuser=OurUser(result)

        if myuser.username==form.username.data:
            print("Username found")
            # if myuser.password== form.password.data:
            if bcrypt.check_password_hash(myuser.password, form.password.data):
                print("Password matched")
                user=User(myuser.user_id)
                login_user(user)
                print("Logiin sucess")
                # error="Logiin sucess"
                # flash("you are successfuly logged in")  
                curr.close()
                session['username'] = myuser.username
                return redirect(url_for('home'))
            else:
                curr.close()
                error="Wrong Password"
        else:
            curr.close()
            error="Wrong Username"      
    return render_template('login.html', form=form)
     
    # return render_template("login.html")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()

    return 'Logged out successfully'

@app.route('/Register')
def Register():
    return render_template("Register.html")


@app.route('/AboutUs')

def AboutUs(): 
    return render_template("AboutUs.html")

@app.route('/addLab')
@login_required
def addLab():
    return render_template("addLab.html")

@app.route('/addSoftware')

def addSoftware():
    return render_template("addSoftware.html")

@app.route('/LabListing')

def LabListing():
    return render_template("LabListing.html")

@app.route('/labdetails')

def labdetails():
    return render_template("labdetails.html")

@app.route('/softwaredetails')

def softwaredetails():
    return render_template("softwaredetails.html")

@app.route('/SoftwareListing')

def SoftwareListing():
    return render_template("SoftwareListing.html")

@app.route('/myaccount')

def myaccount():
    return render_template("myaccount.html")

if __name__ == "__main__":
    app.run(debug=True,port=8000)


