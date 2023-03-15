from . import restaurant
from app import mysql
from flask import jsonify

@restaurant.route('/restaurants', methods=["GET"])
def get_restaurants():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name FROM restaurant')
    restaurants = cursor.fetchall()
    cursor.close()
    return jsonify(restaurants)