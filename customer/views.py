from . import customer
from flask import render_template
from app import mysql


@customer.route('/users')
def users():
    return 'Welcome users'

@customer.route('/dashboard')
def dashboard():
    return render_template("customer/dashboard.html")
