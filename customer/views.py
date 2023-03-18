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
        cursor.execute("select distinct r.restaurant_ID, r.name, r.email, r.phone_number, r.rating, address.city, address.pin_code, address.state from restaurant r inner join address on r.rest_address = address.address_ID inner join cuisine_type ct on r.restaurant_ID = ct.restaurant_ID where ct.type = %s and r.rating >= ( select avg(rating) from restaurant inner join cuisine_type on restaurant.restaurant_ID = cuisine_type.restaurant_ID where cuisine_type.type = %s ) order by r.rating DESC;", (cuisine, cuisine))
        rest_details = cursor.fetchall()

    rests = []
    for detail in rest_details:
        temp = {
            'ID': detail[0],
            'name':detail[1],
            'email': detail[2],
            'phone': detail[3],
            'rating': detail[4],
            'city': detail[5],
            'pincode': detail[6],
            'state': detail[7]
        }
        print(temp)
        rests.append(temp)
    return render_template('customer/restlist.html', rests=rests)

@customer.route('/menu', methods=['GET', 'POST'])
def getmenu():
    if (request.values.get("restaurant")):
        rest_ID = request.values.get("restaurant")
        cursor = mysql.connection.cursor()
        cursor.execute("select name from restaurant where restaurant_ID = %s;", [rest_ID])
        rest = cursor.fetchone()
        rest_name = rest[0]
        cursor.execute("select name, unit_price, veg, item_type, item_ID from menu_item where restaurant_ID = %s and menu_item.availability='1';", [rest_ID])
        menu_items = cursor.fetchall()
        items = []
        for item in menu_items:
            temp = {
                'name': item[0],
                'unit_price': item[1],
                'veg_nonveg': int(item[2]),
                'type': item[3],
                'ID': item[4]
            }
            items.append(temp)
        return render_template('customer/menu.html', rest_name=rest_name, items=items)
    return render_template('customer/menu.html')

@customer.route('/orderconfirmation', methods=['GET', 'POST'])
def orderconfirmation():
    if (request.method=="POST"):
        cursor = mysql.connection.cursor()
        order_items = []
        total_price = 0
        for item in request.form:
            item_ID = item[0]
            item_quantity = item[1]
            if (item_quantity):
                cursor.execute("select name, unit_price, veg, item_type from menu_item where item_ID = %s;", item_ID)
                menu_item = cursor.fetchone()
                price = int(menu_item[1]) * int(item_quantity)
                order_item = {
                    'name': menu_item[0],
                    'unit_price': menu_item[1],
                    'veg': int(item[2]),
                    'item_type': item[3],
                    'price': price,
                }
                total_price += price
                order_items.append(order_item)
        return render_template("customer/orderconfirmation.html", total_price=total_price, order_items=order_items)


    return render_template("customer/menu.html")
