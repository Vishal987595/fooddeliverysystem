from . import delivery
from flask import render_template

@delivery.route('/agentdetail')
def agentdetail():
    return render_template('delivery/agentdetail.html')