from . import restaurant
from app import mysql
from flask import jsonify, render_template, session

@restaurant.route('/restaurants', methods=["GET"])
def get_restaurants():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name FROM restaurant')
    restaurants = cursor.fetchall()
    cursor.close()
    return jsonify(restaurants)

@restaurant.route('/restdetail')
def restdetail():
    return render_template('restaurant/restdetail.html')

@restaurant.route('/restmenu', methods=["POST"])
def restmenu():

    if (session['restbool']):
        rest_ID = session.get("restaurant_ID")
        cursor = mysql.connection.cursor()
        cursor.execute("select name from restaurant where restaurant_ID = %s;", [rest_ID])
        rest = cursor.fetchone()
        rest_name = rest[0]
        cursor.execute("select order_ID from orders inner join restaurant r on orders.restaurant_ID = r.restaurant_ID where r.restaurant_ID = %s order by orders.order_placed_time DESC; ", [rest_ID])
        return render_template('customer/menu.html', rest_name=rest_name)
    return render_template('restaurant/menu.html')

