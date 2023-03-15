from . import customer
from app import mysql

@customer.route('/users')
def users():
    
    return 'Welcome users'