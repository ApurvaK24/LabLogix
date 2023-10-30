# pip install flask
# pip install flask-mysql
from flaskext.mysql import MySQL
from flask import Flask, flash, render_template,session, url_for, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = "Shooo!This is secretkey"

app.config['MYSQL_DATABASE_HOST']='sql12.freemysqlhosting.net'
app.config['MYSQL_DATABASE_USER']='sql12652718'
app.config['MYSQL_DATABASE_PASSWORD']='DsRaiJa9kh'
app.config['MYSQL_DATABASE_DB']='sql12652718'
mysql = MySQL()

mysql.init_app(app)


curr= mysql.connect().cursor()


# curr.execute("INSERT INTO user (username,password,fname,lname,role) VALUES (%s, %s, %s , %s, %s)", (username, hashed_password, fname, lname,  roleselected))
# mysql.connection.commit()


curr.execute("select * from user where username = %s", ("Ak"))
result = curr.fetchall()
print(result)







curr.close()