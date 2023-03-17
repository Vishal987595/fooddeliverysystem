import time
import datetime
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
        cursor.execute('SELECT Orders.order_ID, Orders.order_placed_time, Orders.order_status, restaurant.name as restaurant_name, order_totals.net_price FROM Orders inner join restaurant on Orders.restaurant_ID = restaurant.restaurant_ID inner join ( SELECT Orders.order_ID, SUM(Menu_Item.unit_price * Order_Items.quantity) AS net_price FROM Orders JOIN Order_Items ON Orders.order_ID = Order_Items.order_ID JOIN Menu_Item ON Order_Items.item_ID = Menu_Item.item_ID GROUP BY Orders.order_ID ) order_totals on Orders.order_ID = order_totals.order_ID WHERE customer_ID = %s ORDER BY order_placed_time DESC;',(ID))
        orders_by_cust = cursor.fetchall()
        orders = []
        for placed_order in orders_by_cust:
            temp = {
                    'rest_name': placed_order[3],
                    'time': placed_order[1].strftime('%Y-%m-%d %H:%M:%S'),
                    'status': placed_order[2],
                    'price': placed_order[4]
            }
            orders.append(temp)
        context = {
            "first_name":account[1],
            "last_name": account[2],
            "email": account[4], 
            "phone_no": account[5], 
            "order_placed": (len(orders) > 0),
        }
        return render_template('customer/userprofile.html', context=context, orders=orders)
    return render_template('customer/userprofile.html')

@customer.route('/resslist')
def resslist():
    return render_template('customer/resslist.html')