from flask import Flask, render_template, request, redirect, url_for, session
import flask

import MySQLdb.cursors

app = Flask(__name__)
from configure import config
mysql = config(app)

from restaurant import restaurant
from customer import customer
from delivery import delivery
app.register_blueprint(restaurant)
app.register_blueprint(customer)
app.register_blueprint(delivery)

@app.route('/home')
def home():
    session.clear()
    return render_template('index.html')


@app.route('/')
def index():
    return redirect(url_for('home'))

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
        session['addr_ID'] = None
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if (authority == "Customer"):
            cursor.execute("SELECT * FROM Customers WHERE email = % s AND password = % s", (useremail, password,))
            account = cursor.fetchone()
            if account:
                session['customerbool'] = True
                session['restbool'], session['agentbool'] = False, False
                session['customer_ID'] = str(account['customer_ID'])
                cursor.execute("select address_ID from customer_address where customer_ID=%s", (session['customer_ID'],))
                addr_ID = cursor.fetchall()
                session['addr_ID'] = addr_ID[0]
                msg = 'Logged in successfully !'
                flask.flash(msg)
                return redirect(url_for('customer.dashboard'))
            else:
                msg = 'Incorrect username / password !'
        elif (authority == "Delivery Agent"):
            cursor.execute("SELECT * FROM delivery_agent WHERE email = % s AND password = % s", (useremail, password, ))
            account = cursor.fetchone()
            if account:
                session['agentbool'] = True
                session['cutomerbool'], session['restbool'] = False, False
                session['agent_ID'] = account['agent_ID']
                msg = 'Logged in successfully !'
                flask.flash(msg)
                return redirect(url_for('delivery.agentdetail'))
            else:
                msg = 'Incorrect username / password !'
        elif (authority == "Restaurant"):
            cursor.execute("SELECT * FROM restaurant WHERE email = % s AND password = % s", (useremail, password, ))
            # cursor.execute(f"SELECT * FROM restaurant WHERE email='{useremail}' AND password='{password}'")
            account = cursor.fetchone()
            if account:
                session['restbool'] = True
                session['agentbool'], session['customerbool'] = False, False
                session['restaurant_ID'] = account['restaurant_ID']
                msg = 'Logged in successfully !'
                flask.flash(msg)
                return redirect(url_for('restaurant.restdetail'))
            else:
                msg = 'Incorrect username / password !'
        else:
            msg = 'Incorrect username / password !'
        flask.flash(msg)
    return render_template('login.html', msg = msg)


# making routes for sign up for all three types of users
@app.route('/signupcustomer',methods=['GET', 'POST'])
def signupcustomer():
    if request.method == 'POST':
        msg = 'CUSTOMER: Please fill out the form again'
        userdetails = request.form
        firstname = userdetails['firstname']
        lastname = userdetails['lastname']
        email = userdetails['email']
        DOB = userdetails['DOB']
        phone_number = userdetails['phone_number']
        password = userdetails['password']
        building_name = userdetails['building_name']
        street_name = userdetails['street_name']
        city = userdetails['cityname']
        state = userdetails['statename']
        pin_code = userdetails['pincode']
        cur = mysql.connection.cursor()
        cur.execute("select max(customer_ID) from customers")
        ID = cur.fetchone()
        ID = str(int(ID[0]) + 1)
        cur.execute("select address_ID from address where building_name=%s and street_name=%s and pin_code=%s and city=%s and state=%s", (building_name, street_name, pin_code, city, state))
        address_ID = cur.fetchone()
        try:
            if (address_ID == None):
                cur.execute("select max(address_ID) from address")
                address_ID = cur.fetchone()
                address_ID = str(int(address_ID[0]) + 1)
                cur.execute("insert into address(address_ID, building_name, street_name, pin_code, city, state) values(%s, %s, %s, %s, %s, %s)", (address_ID, building_name, street_name, pin_code, city, state))
                mysql.connection.commit()
            else:
                address_ID = address_ID[0]
            cur.execute("insert into customers(customer_ID, first_name, last_name, email, phone_no, password, DOB) values(%s, %s, %s, %s, %s , %s, %s)", (ID, firstname, lastname, email, phone_number, password, DOB))
            cur.execute("insert into customer_address(customer_ID, address_ID) values(%s, %s);", (ID, address_ID,))
            mysql.connection.commit()
        except:
            flask.flash(msg)
            return render_template('customersignup.html')
        mysql.connection.commit()
        cur.close()
        msg = 'CUSTOMER: signup successfully!!'
        flask.flash(msg)
        return redirect(url_for('login'))
    return render_template('customersignup.html')

@app.route('/signuprestaurant', methods=['GET', 'POST'])
def signuprestaurant():
    if request.method == 'POST':
        msg = 'Restaurant please fill out the form again'
        restdetail = request.form
        name = restdetail['name']
        email = restdetail['email']
        phoneno = restdetail['Phone number']
        password = restdetail['password']
        # Keeping weekend_time and weekday_time as null values
        # For now keeping rest_address from our side
        cur = mysql.connection.cursor()
        cur.execute('select max(restaurant_ID) from restaurant')
        ID = cur.fetchone()
        ID = str(int(ID[0]) + 1)
        building_name = restdetail['buildingnumber']
        street_name = restdetail['streetname']
        city = restdetail['cityname']
        state = restdetail['statename']
        pin_code = restdetail['pincode']
        cur.execute("select address_ID from address where building_name=%s and street_name=%s and pin_code=%s and city=%s and state=%s", (building_name, street_name, pin_code, city, state))
        address_ID = cur.fetchone()
        try:
            if (address_ID == None):
                cur.execute("select max(address_ID) from address")
                address_ID = cur.fetchone()
                rest_address = str(int(address_ID[0]) + 1)
                cur.execute("insert into address(address_ID, building_name, street_name, pin_code, city, state) values(%s, %s, %s, %s, %s, %s)", (rest_address, building_name, street_name, pin_code, city, state))
                mysql.connection.commit()
            else:
                rest_address = address_ID[0]
            cur.execute('insert into restaurant(restaurant_ID, name, email, phone_number, rest_address, password, weekday_time, weekend_time) values(%s, %s, %s, %s, %s, %s, 7, 8)', (ID, name, email, phoneno, rest_address, password))
        except:
            flask.flash(msg)
            return render_template('restaurantsignup.html')
        mysql.connection.commit()
        cur.close()
        msg = 'RESTAURANT signup successfully!!'
        flask.flash(msg)
        return redirect(url_for('login'))
    return render_template('restaurantsignup.html')

@app.route('/signupdeliveryagent', methods=['GET', 'POST'])
def signupdeliveryagent():
    if request.method == 'POST':
        msg = 'Agent please fill out the form again'
        agentdetail = request.form
        cur = mysql.connection.cursor()
        cur.execute('select max(agent_ID) from delivery_agent;')
        ID = cur.fetchone()
        ID = str(int(ID[0]) + 1)
        building_name = agentdetail['buildingnumber']
        street_name = agentdetail['streetname']
        city = agentdetail['cityname']
        state = agentdetail['statename']
        pin_code = agentdetail['pincode']
        cur.execute("select address_ID from address where building_name=%s and street_name=%s and pin_code=%s and city=%s and state=%s", (building_name, street_name, pin_code, city, state))
        address_ID = cur.fetchone()
        try:
            if (address_ID == None):
                cur.execute("select max(address_ID) from address")
                address_ID = cur.fetchone()
                address_ID = str(int(address_ID[0]) + 1)
                cur.execute("insert into address(address_ID, building_name, street_name, pin_code, city, state) values(%s, %s, %s, %s, %s, %s)", (address_ID, building_name, street_name, pin_code, city, state))
                mysql.connection.commit()
            else:
                address_ID = address_ID[0]
            cur.execute('insert into delivery_agent(agent_ID, first_name, middle_name, last_name, phone_no, email, DOB, password, address_ID) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', (ID, agentdetail['firstName'], agentdetail['MiddleName'], agentdetail['lastName'], agentdetail['Phone number'], agentdetail['email'], agentdetail['DOB'], agentdetail['password'], address_ID))
            mysql.connection.commit()
        except:
            flask.flash(msg)
            return render_template('deliveryagentsignup.html')
        mysql.connection.commit()
        cur.close()
        msg = 'AGENT signup successfully!!'
        flask.flash(msg)
        return redirect(url_for('login'))
    return render_template('deliveryagentsignup.html')

# about us url
@app.route('/aboutus', methods=["GET", "POST"])
def aboutus():
    if (request.method=="POST"):
        cur = mysql.connection.cursor()
        renaming_col =str( request.values.get("col_name"))
        rename_value =str( request.values.get("new_name"))
        if (rename_value != ""):
            query = f"ALTER TABLE `team_details` RENAME COLUMN `{renaming_col}` TO `{rename_value}`;"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            flask.flash("Successfully renamed the column")
        else:
            flask.flash("Please put up rename value of the column.")
    query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s"
    tablename = 'Team_details'  
    cur = mysql.connection.cursor()
    cur.execute(query, ("Team_details",))
    col_name = cur.fetchall()

    table ={
        'col1':col_name[0][0],
        'col2':col_name[1][0],
        'col3':col_name[2][0],
        'col4':col_name[3][0],
    }
    query = f"SELECT `{table['col1']}`, `{table['col2']}`, `{table['col3']}`, `{table['col4']}` FROM `team_details`;"
    cur.execute(query)
    students = cur.fetchall()
    student_details=[]
    for student in students:
        temp = {
            'col1':student[0],
            'col2':student[1],
            'col3':student[2],
            'col4':student[3]
        }
        student_details.append(temp)
    
    return render_template('aboutus.html',tablename=tablename, table = table, student_details= student_details)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)