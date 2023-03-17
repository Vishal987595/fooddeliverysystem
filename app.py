from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import flask
import yaml
import MySQLdb.cursors
import re

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.secret_key = 'your secret key'
mysql = MySQL(app)

from restaurant import restaurant
from delivery import delivery
from customer import customer
app.register_blueprint(customer)
app.register_blueprint(delivery)
app.register_blueprint(restaurant)

@app.route('/')
def index():
    return "This is an example app"

@app.route('/home')
def home():
    return render_template('index.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')






@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'useremail' in request.form and 'password' in request.form and 'authority' in request.form:
        useremail = request.form['useremail']
        password = request.form['password']
        authority = request.form['authority']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if (authority == "Customer"):
            cursor.execute('SELECT * FROM Customers WHERE email = % s AND password = % s', (useremail, password, ))
            account = cursor.fetchone()
            if account:
                session['bool'] = True
                session['customer_ID'] = account['customer_ID']
                msg = 'Logged in successfully !'
                flask.flash(msg)
                return redirect(url_for("customer.dashboard"))
            else:
                msg = 'Incorrect username / password !'
        elif (authority == "Delivery Agent"):
            cursor.execute('SELECT * FROM delivery_agent WHERE email = % s AND password = % s', (useremail, password, ))
            account = cursor.fetchone()
            if account:
                session['bool'] = True
                session['agent_ID'] = account['agent_ID']
                msg = 'Logged in successfully !'
                flask.flash(msg)
                return render_template('index.html', message=msg)
            else:
                msg = 'Incorrect username / password !'
        elif (authority == "Restaurant"):
            cursor.execute('SELECT * FROM restaurant WHERE email = % s AND password = % s', (useremail, password, ))
            account = cursor.fetchone()
            if account:
                session['bool'] = True
                session['restaurant_ID'] = account['restaurant_ID']
                msg = 'Logged in successfully !'
                flask.flash(msg)
                return render_template('index.html', message=msg)
            else:
                msg = 'Incorrect username / password !'
        else:
            msg = 'Incorrect username / password !'
            flask.flash(msg)
    return render_template('login.html', msg = msg)


# making rout for sign up for all three types of users
@app.route('/signupcustomer',methods=['GET', 'POST'])
def signupcustomer():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('customersignup.html')

@app.route('/signupreastaurant')
def signupreastaurant():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('restaurantsignup.html')

@app.route('/signupdeliveryagent')
def signupdeliveryagent():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('deliveryagentsignup.html')

# about us url
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

if __name__ == '__main__':
    app.run(debug=True)