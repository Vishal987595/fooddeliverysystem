from . import customer
from flask import render_template, session, flash, redirect
from app import mysql

@customer.route('/users')
def users():
    return 'Welcome users'

@customer.route('/dashboard')
def dashboard():
    cursor = mysql.connection.cursor()
    cursor.execute('select distinct type from cuisine_type')
    output = cursor.fetchall()
    cuisines = []
    for i in range(len(output)):
        p = str(output[i])
        print(output[i])
        cuisines.append(p[2:-3])
    return render_template("customer/dashboard.html", cuisines=cuisines)

@customer.route('/userprofile')
def userprofile():
    ID = session['customer_ID']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Customers WHERE customer_ID = % s', (ID))
    account = cursor.fetchone()
    if account:
        context = {
            "first_name":account[1],
            "last_name": account[2],
            "email": account[4], 
            "phone_no": account[5], 
            "order_placed": False,
        }
        print(context)
        return render_template('customer/userprofile.html', context=context)
    return render_template('customer/userprofile.html')