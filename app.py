from flask import Flask,render_template,flash,session, request, logging
import serial
import datetime
from passlib.hash import sha256_crypt

import mysql.connector
from flask import Flask, render_template, url_for, flash, redirect,request
from forms import RegistrationForm, LoginForm,AjouterForm
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap



@app.route('/presence')
@is_logged_in
def fetcha():
    db_connection = mysql.connector.connect(host="localhost",user="root",passwd="",db='school')
    cur=db_connection.cursor()
    query="""SELECT * FROM attendance """
    cur.execute(query)
    data=cur.fetchall()
    return render_template('presence.html', attendance=data)



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        name = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # Create cursor
        db_connection = mysql.connector.connect(host="localhost",user="root",passwd="",db='school')
        cur=db_connection.cursor()
        # Execute query
        cur.execute("INSERT INTO users(username, email, password) VALUES( %s, %s, %s)", (name, email, password))

        # Commit to DB
        db_connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        db_connection = mysql.connector.connect(host="localhost",user="root",passwd="",db='school')
        cur=db_connection.cursor()

        # Get user by username
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        result=cur.fetchall()
        print(result)

        if len(result) > 0:
            for id,username,email,password in result:
                # Compare Passwords
                if sha256_crypt.verify(password_candidate, password):
                    # Passed
                    session['logged_in'] = True
                    session['username'] = username

                    flash('You are now logged in', 'success')
                    return redirect(url_for('ajouter'))
            else:
                    error = 'Invalid login'
                    return render_template('login.html', error=error)
                # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')




@app.route('/getRfid')
@is_logged_in
def readrfid():
    while True:
        ser = serial.Serial("COM3",9600)
        thing = ser.readline().rstrip()
        idc=thing.decode(encoding="utf-8",errors="strict")
        print(idc)
        if len(idc)==13:
            break
    return {"RFID":idc}

 
@app.route("/ajouter", methods=['GET', 'POST'])
@is_logged_in
def ajouter():
    form = AjouterForm()
    if request.method =='GET':
        db_connection = mysql.connector.connect(host="localhost",user="root",passwd="",db='school')
        cur=db_connection.cursor()
        query="""SELECT * FROM etudiant"""
        cur.execute(query)
        data=cur.fetchall()        

    if request.method =='POST':
        etudiant=request.form
        name=etudiant['nom']
        rfid=etudiant['rfid']
        cne=etudiant['cne']
        db_connection = mysql.connector.connect(host="localhost",user="root",passwd="",db='school')
        cur=db_connection.cursor()
        query="""INSERT INTO etudiant (nom,CNE,num) values (%s,%s,%s)"""
        cur.execute(query,(name,cne,rfid))
        db_connection.commit()
        flash('Etudiant Ajouter')
        return redirect(request.url)
    return render_template('home.html', title='Register', form=form,data=data)

if __name__ == '__main__':
    app.run(debug=True)


