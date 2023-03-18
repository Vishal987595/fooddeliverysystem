from . import customer
from flask import render_template, session, request
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
    cursor.execute("SELECT * FROM Customers WHERE customer_ID = %s", (ID,))
    account = cursor.fetchone()
    if account:
        cursor.execute("SELECT Orders.order_ID, Orders.order_placed_time, Orders.order_status, restaurant.name as restaurant_name, order_totals.net_price FROM Orders inner join restaurant on Orders.restaurant_ID = restaurant.restaurant_ID inner join ( SELECT Orders.order_ID, SUM(Menu_Item.unit_price * Order_Items.quantity) AS net_price FROM Orders JOIN Order_Items ON Orders.order_ID = Order_Items.order_ID JOIN Menu_Item ON Order_Items.item_ID = Menu_Item.item_ID GROUP BY Orders.order_ID ) order_totals on Orders.order_ID = order_totals.order_ID WHERE customer_ID = (%s) ORDER BY order_placed_time DESC;",(ID,))
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


# Getting the restaurant list with rating >= Avg rating
@customer.route('/restlist', methods=['GET'])
def restlist():
    if (request.values.get("query")):
        query = request.values.get("query")
        query = "%" + query + "%"
        cursor = mysql.connection.cursor()
        cursor.execute("select r.name, r.email, r.phone_number, r.rating, address.city, address.pin_code, address.state from restaurant r inner join address on r.rest_address = address.address_ID where r.name like %s ;", (query,))
        rest_details = cursor.fetchall()    
    else:
        cuisine = request.values.get("cuisine")
        cursor = mysql.connection.cursor()
        cursor.execute("select distinct r.name, r.email, r.phone_number, r.rating, address.city, address.pin_code, address.state from restaurant r inner join address on r.rest_address = address.address_ID inner join cuisine_type ct on r.restaurant_ID = ct.restaurant_ID where ct.type = %s and r.rating >= ( select avg(rating) from restaurant inner join cuisine_type on restaurant.restaurant_ID = cuisine_type.restaurant_ID where cuisine_type.type = %s ) order by r.rating DESC;", (cuisine, cuisine))
        rest_details = cursor.fetchall()

    rests = []
    for detail in rest_details:
        temp = {
            'name':detail[0],
            'email': detail[1],
            'phone': detail[2],
            'rating': detail[3],
            'city': detail[4],
            'pincode': detail[5],
            'state': detail[6]
        }
        rests.append(temp)
    return render_template('customer/restlist.html', rests=rests)