from . import restaurant
from app import mysql
from flask import jsonify, render_template, session, flash

@restaurant.route('/restaurants', methods=["GET"])
def get_restaurants():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name FROM restaurant')
    restaurants = cursor.fetchall()
    cursor.close()
    return jsonify(restaurants)

@restaurant.route('/restdetail', methods=["GET"])
def restdetail():
    ans = False
    try:
        ans = session['restbool']
        rest_ID = session['restaurant_ID']
        rest_name = False
    except: 
        msg = "Need to login as restaurant"
        flash(msg)
        return render_template('restaurant/restdetail.html', rest_name=rest_name)

    cur = mysql.connection.cursor()
    cur.execute("select name from restaurant where restaurant_ID=%s;",(rest_ID,))
    rest_name = cur.fetchone()[0]
    cur.execute("SELECT Orders.order_ID, Orders.order_placed_time, Orders.order_status, order_totals.net_price FROM Orders inner join restaurant on Orders.restaurant_ID = restaurant.restaurant_ID inner join ( SELECT Orders.order_ID, SUM(Menu_Item.unit_price * Order_Items.quantity) AS net_price FROM Orders JOIN Order_Items ON Orders.order_ID = Order_Items.order_ID JOIN Menu_Item ON Order_Items.item_ID = Menu_Item.item_ID GROUP BY Orders.order_ID ) order_totals on Orders.order_ID = order_totals.order_ID WHERE Orders.restaurant_ID = %s ORDER BY order_placed_time DESC LIMIT 10;", (rest_ID,))
    orders_rest = cur.fetchall()
    orders = []
    for order in orders_rest:
        temp = {
            'order_placed_time':order[1],
            'order_status': order[2],
            'net_price': order[3], 
        }
        items = []
        cur.execute("select name, unit_price, quantity from order_items left join menu_item on order_items.item_ID=menu_item.item_ID where order_items.order_ID=%s;", (order[0],))
        order_items = cur.fetchall()
        for order_item in order_items:
            it = {
                'name': order_item[0],
                'unit_price': order_item[1],
                'quantity': order_item[2],
            }
            items.append(it)
        temp['order_items'] = items
        orders.append(temp)
    return render_template('restaurant/restdetail.html', rest_name=rest_name, orders=orders)

@restaurant.route('/restmenu', methods=["GET", "POST"])
def restmenu():
    if (session['restbool']):
        rest_ID = session.get("restaurant_ID")
        cursor = mysql.connection.cursor()
        cursor.execute("select name from restaurant where restaurant_ID = %s;", [rest_ID])
        rest = cursor.fetchone()
        rest_name = rest[0]
        cursor.execute("select name, unit_price, veg, item_type, item_ID from menu_item where restaurant_ID = %s;", [rest_ID])
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
        return render_template('restaurant/menu.html', rest_name=rest_name, items=items)
    return render_template('restaurant/menu.html')

