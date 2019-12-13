from flask import Flask,render_template
import serial
import datetime
import mysql.connector

app= Flask(__name__)


@app.route("/")
def index():
    form =addETudiant()
    return render_template('home.html',title="Home",form=form)

@app.route("/ajouter")
def addETudiant():
    return "Add Etudiant!"

@app.route('/getRfid')
def readrfid():
    while True:
        ser = serial.Serial("com3",9600)
        thing = ser.readline().rstrip()
        idc=thing.decode(encoding="utf-8",errors="strict")
        print(idc)
        if len(idc)==13:
            break
    return {"RFID":idc}
