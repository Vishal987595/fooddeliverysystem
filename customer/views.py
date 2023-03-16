from . import customer
from flask import render_template
from app import mysql

@customer.route('/users')
def users():
    return 'Welcome users'

@customer.route('/dashboard')
def dashboard():
    cursor = mysql.connection.cursor()
    cursor.execute('select distinct type  from cuisine_type')
    output = cursor.fetchall()
    cuisines = []
    for i in range(len(output)):
        p = str(output[i])
        cuisines.append(p[2:-3])
    return render_template("customer/dashboard.html", cuisines=cuisines)

@customer.route('/userprofile')
def userprofile():
    return render_template('customer/userprofile.html')