from . import delivery

@delivery.route('/details')
def details():
    return "delivery orders"