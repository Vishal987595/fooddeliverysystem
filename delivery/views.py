from . import delivery
from app import mysql
from flask import render_template, session, flash, request

@delivery.route('/agentdetail', methods=["GET"])
def agentdetail():
    ans = False
    try:
        ans = session['restbool']
        agent_ID = session['agent_ID']
        agent_name = False
        print("try")
    except: 
        msg = "Need to login as restaurant"
        flash(msg)
        print("except")
        return render_template('delivery/agentdetail.html', agent_name=agent_name)

    cur = mysql.connection.cursor()
    cur.execute("select agent_ID, first_name, last_name, email, phone_no, address_ID from delivery_agent where agent_ID=%s;",(agent_ID,))
    agent_detail = cur.fetchone()
    
    
    agent_id = agent_detail[0]
    query = "SELECT * FROM orders WHERE order_id IN (SELECT order_id FROM delivery_agent WHERE agent_id = %s) ORDER BY order_placed_time DESC"
    cur.execute(query, (agent_id,))
    orders_rest = cur.fetchall()
    
    return render_template('delivery/agentdetail.html', agent_detail=agent_detail )

