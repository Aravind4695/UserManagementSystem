# connect python into mysql

# import mysql.connector
# sql = mysql.connector.connect(host='localhost', user='root', password='happy', database='users');

#check the connection either connected or not
# if con:
#     print('connected');
# else:
#     print('not connected')

from flask import Flask, render_template, request, url_for, redirect,flash
from flask_mysqldb import MySQL

app = Flask(__name__)
# connecting mysql with flask (using - from flask_mysqldb import MySQL )
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "happy"
app.config["MYSQL_DB"] = "users"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route('/')    # @app.route('/') - tells which page running in the browser
def home():
    con = mysql.connection.cursor()
    qry = "select * from users1"
    con.execute(qry)
    res = con.fetchall()
    return render_template("home.html", datas=res)  # render_template - connecting the files & used to send the data

@app.route("/addUser", methods=["POST", "GET"])
def add():
    if request.method == "POST":  # request - this module used to check the methods and get the vakue from form
        name = request.form ['name']
        age = request.form ['age']
        city = request.form ['city']
        con = mysql.connection.cursor()
        qry = "insert into users1 (NAME,AGE,CITY) values (%s,%s,%s)"
        con.execute(qry, [name, age, city])
        mysql.connection.commit()
        con.close()
        flash('User detail added successfully')
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route('/editUser/<string:id>',methods=["POST","GET"])
def edit(id):
    con = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        qry = "update users1 set NAME = %s, AGE = %s, CITY = %s where ID = %s"
        con.execute(qry, [name, age, city, id])
        mysql.connection.commit()
        con.close()
        flash('User detail updated successfully')
        return redirect(url_for('home'))
    qry = "select * from users1 where ID= %s"
    con.execute(qry, [id])
    res = con.fetchone()
    return render_template('edit.html', data=res)
@app.route('/deleteUser/<string:id>',methods=['GET','POST'])
def delete(id):
    con = mysql.connection.cursor()
    qry = "delete from Users1 where ID = %s"
    con.execute(qry, [id])
    mysql.connection.commit()
    con.close()
    flash('User detail deleted successfully')
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.secret_key = 'zaq123'
    app.run(debug=True)