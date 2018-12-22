# -*- coding: utf-8 -*-
"""
@author: Enrique Martín Martín
@email: emartinm@ucm.es
"""

from bottle import run, get, post, request
import sqlite3


# Ejemplo de XSS persitente
# Pasos:
# 1. Insertar un mensaje conteniendo código JavaScript
#    http:/localhost:8080/insert_message
#	(por ejemplo "<script>alert("Peligro");</script>")
# 2. Visualizar el mensaje recién creado
#    http:/localhost:8080/show_message?id=2


@get('/insert_message')
def insert_form():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Insert message</title>
</head>
<body>
 <form action="http://localhost:8080/insert_message" method="post">
  Author:<br>
  <input type="text" name="author" value="pepe">
  <br>
  Title:<br>
  <input type="text" name="title" value="Duda existencial">
  <br>
  Body:<br>
  <textarea name="body" rows="10" cols="50">Alguien sabe lo que significa 
<script>alert("Peligro");</script></textarea>
  <br>
  <br><br>
  <input type="submit" value="Submit">
</form> 
</body>
</html>"""


@post('/insert_message')
def insert_message():
    qbody = "INSERT INTO messages(author, title, body) VALUES ('{0}', '{1}', '{2}')"
    author = request.forms['author']
    title = request.forms['title']
    body = request.forms['body']
    query = qbody.format(author, title, body)
    
    try: 
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(query)
        msg_id = cur.lastrowid
        conn.commit()
        conn.close()
            
        return "Mensaje insertado con ID " + str(msg_id)
    except:
        return "Error al insertar el mensaje"


@get('/show_message')
def show_message():
    msg_id = request.query['id']
    query = "SELECT * FROM messages WHERE id='{0}'".format(msg_id)
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchone()
    conn.commit()
    conn.close()
    
    html = "<ul><li>Author: {0}</li><li>Title: {1}</li><li>Body: {2}</li></ul>"
    html = html.format(*row[1:])
    
    return html
    

if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)
