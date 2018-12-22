# -*- coding: utf-8 -*-
"""
@author: Enrique Martín Martín
@email: emartinm@ucm.es
"""

from bottle import get, run, request
import sqlite3


# Inyección SQL:
# http://localhost:8080/orders?user=pepe%27%20or%20%27a%27=%27a
@get('/orders')
def orders():
    u = request.query['user']
    qbody = "SELECT * FROM orders WHERE user='{0}'"
    query = qbody.format(u)
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query)
    listing = ""
    for row in cur:
        listing += "ID:{0} -> user:{1} - item: {2}<br/>".format(*row)
    conn.close()
    
    return listing
    
    
if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
