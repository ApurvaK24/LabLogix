from flask import Flask, render_template
# from flask_wtf import FlaskForm
# from wtforms import StringField , SubmitField
# from wtforms.validators import DataRequired


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


