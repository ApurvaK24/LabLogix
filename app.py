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
from wtforms import DateField, DecimalField, IntegerField, SelectField, StringField, PasswordField, SubmitField, TextAreaField
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
    fname = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "First Name"})
    lname = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": " Last Name"})
    username = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Password"})
    repassword = PasswordField(validators=[
                             InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Re-enter Password"})
    role = SelectField(u'Select Role', choices=[('Admin', 'Admin'), ('Professor', 'Professor'), ('Assistant', 'Assistant')])
    submit = SubmitField('Register')

    def validateusername(self):
        # pass
        username=self.username
        curr= mysql.connect().cursor()
        curr.execute("select * from user where username='{}'".format(username))
        result = curr.fetchall()
        myuser=OurUser(result)
        curr.close()
        
        if username==myuser.username:
            flash("That username already exists. Please choose a different one.")
            print("That username already exists. Please choose a different one.")
            # raise ValidationError(
            #     'That username already exists. Please choose a different one.')
            return False
        else:
            return True
    def validatesecondpassword(self):
        # print(self.password.data,self.repassword.data)
        if(self.password.data==self.repassword.data):
            return True
        else:
            print("Password and repassword not matched")
            return False
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Username"})
    # username = StringField(validators=[
    #                        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired()],  render_kw={"placeholder": "Password"})

    role = SelectField(u'Select Role', choices=[('Admin', 'Admin'), ('Professor', 'Professor'), ('Assistant', 'Assistant')])

    submit = SubmitField('Submit')

class addLabForm(FlaskForm):
    labname = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Enter Lab Name"})
    labmanager = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Enter Lab Manager"})
    lab_location = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Enter Lab Location"})
    description = TextAreaField(render_kw={"placeholder": "Enter Lab description"})
    # username = StringField(validators=[
    #                        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    no_of_pc = IntegerField(render_kw={"placeholder": "Enter Number of PC's"})

    submit = SubmitField('Submit')
class addSoftwareForm(FlaskForm):
    software_name = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Enter Software Name"})
    lab_name = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Enter Lab Name"})

    software_manager = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Enter Software Manager Name"})
    software_key = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Enter Software Key"})
    
    cost = DecimalField(validators=[
                           InputRequired()],render_kw={"placeholder": "Enter Software Cost "})
    availability = IntegerField(validators=[
                           InputRequired()],render_kw={"placeholder": "Enter Software Availability"})
    valid_up_to = DateField(format='%Y-%m-%d')

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
            self.fname = tupp[0][3]
            self.lname = tupp[0][4]
            self.role = tupp[0][5]
        
        except:
            self.user_id = None
            self.username = None
            self.password = None
            self.fname = None
            self.lname =None
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
                session['id'] = myuser.user_id
                session['username'] = myuser.username
                session['fname']=myuser.fname
                session['lname']=myuser.lname
                return redirect(url_for('home'))
            else:
                curr.close()
                error="Wrong Password"
        else:
            curr.close()
            error="Wrong Username"      
    return render_template('login.html', form=form)
     
    # return render_template("login.html")




@app.route('/Register', methods=['GET', 'POST'])
def Register():
    if (session ):
        if(session['username'] !=None):
            #show message user is loged in already
            flash("You are logged in already") 
            print("You are logged in already") 
            return redirect(url_for('home'))
    curr= mysql.connect().cursor()
    form=RegisterForm()
    if form.validate_on_submit():
        curr= mysql.connect().cursor()
        fname=form.fname.data
        lname=form.lname.data
        username=form.username.data
        password=form.password.data
        repassword=form.repassword.data
        roleselected=form.role.data
        if(form.validateusername() and form.validatesecondpassword()):
            hashed_password = bcrypt.generate_password_hash(password)
            print(fname,lname,username,password,repassword,roleselected)
            curr.execute("INSERT INTO user (username,password,fname,lname,role) VALUES (%s, %s, %s , %s, %s)", (username, hashed_password, fname, lname,  roleselected))
            mysql.connection.commit()
            curr.close()
            # curr.execute("select * from user where username='{}'".format(username))
            # result = curr.fetchall()
            # myuser=OurUser(result)
            flash("User registered, Continue Login")
            return redirect(url_for('login'))
            
        pass
    return render_template("Register.html", form=form)

def clearsessions():
    session['id'] = None
    session['username'] = None
    session['fname']=None
    session['lname']=None

@app.route('/logout')
@login_required
def logout():
    logout_user()
    clearsessions()
    flash("Logged out successfully")
    return render_template("home.html")


@app.route('/AboutUs')

def AboutUs(): 
    return render_template("AboutUs.html")

@app.route('/addLab', methods=['GET', 'POST'])
@login_required
def addLab():
    curr= mysql.connect().cursor()

    form = addLabForm()
    warning=""
    able=True
    id=session['id']
    curr.execute("select * from user where id={}".format(id))
    result = curr.fetchall()
    myuser=OurUser(result)

    if myuser.role=="Admin":
        warning=" "
        able=True
    else:
        warning="Only admin can add Lab"
        able=False
    if form.validate_on_submit():
        if able:
            curr= mysql.connect().cursor()
            labname=form.labname.data
            labmanager=form.labmanager.data
            lab_location=form.fname.data
            description=form.description.data
            no_of_pc=form.no_of_pc.data
            curr.execute("INSERT INTO lablisting (labname,labmanager,lab_location,description,no_of_pc) VALUES (%s, %s, %s , %s, %s)", (labname,labmanager,lab_location,description,no_of_pc))
            mysql.connection.commit()
            print(form.labname.data,form.description.data,form.no_of_pc.data)
            curr.close()
            warning="Lab Added Successfully"
            flash("Lab Added Successfully")
            return redirect(url_for('LabListing'))
    return render_template("addLab.html",form=form,warning=warning,able=able)

@app.route('/addSoftware', methods=['GET', 'POST'])

def addSoftware():
    form=addSoftwareForm()
    if form.validate_on_submit():
        print(form.software_name.data,form.cost.data,form.valid_up_to.data)
    return render_template("addSoftware.html",form=form)

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
@login_required
def myaccount():
    id=session['id']
    curr= mysql.connect().cursor()
    curr.execute("select * from user where id='{}'".format(id))
    result = curr.fetchall()
    myuser=OurUser(result)
    curr.close()
    return render_template("myaccount.html",myuser=myuser)

if __name__ == "__main__":
    app.run(debug=True,port=8000)


