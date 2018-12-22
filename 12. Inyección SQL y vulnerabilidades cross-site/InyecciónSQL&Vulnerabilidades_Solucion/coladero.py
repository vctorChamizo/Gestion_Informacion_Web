# -*- coding: utf-8 -*-
"""
@title: El Coladero
@description: Aplicación web para detectar y corregir vulnerabilidades
@author: Enrique Martín Martín
@email: emartinm@ucm.es
"""

from bottle import run, template, get, post, request
import sqlite3
import os

DBPATH  = 'database.db'
SQLPATH = 'database.sql'

##########################
## FUNCIONES AUXILIARES ##
##########################
# Elimina el fichero database.db (si existe) y lo crea con los valores por defecto
def reset_database():
  try: 
    os.remove(DBPATH)
  except FileNotFoundError:
    pass
    
  conn = sqlite3.connect(DBPATH)
  cur = conn.cursor()
  script_file = open(SQLPATH, 'r')
  script = script_file.read()
  script_file.close()
  cur.executescript(script)
  conn.commit()
  conn.close()
##########################


@get('/show_all_questions')
def show_all_questions():
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    query = """SELECT author,title,time,tags,id 
               FROM Questions 
               ORDER BY time DESC"""
    cur.execute(query)
    res = list(cur.fetchall())
    conn.close()
    return template('messages.html', questions=res)
    

@post('/insert_question')
def insert_question():
    author = request.forms['author']
    title = request.forms['title']
    tags = request.forms['tags']
    body = request.forms['body']
        
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    qbody = """INSERT INTO Questions(author, title, tags, body, time) 
               VALUES ('{0}','{1}','{2}','{3}',CURRENT_TIMESTAMP)"""
    query = qbody.format(author, title, tags, body)
    cur.executescript(query)
    conn.commit()
    conn.close()
    return "Pregunta insertada con exito"

        
@get('/show_question')
def show_question():
    ident = request.query['id']
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    qbody1 = """SELECT author,title,time,tags,body 
                FROM Questions 
                WHERE id=:ident"""
    qbody2 = """SELECT author,time,body 
                FROM Replies 
                WHERE question_id=:ident"""
    params = {'ident' : ident}
    cur.execute(qbody1, params)
    question = cur.fetchone()
    cur.execute(qbody2, params)
    replies = list(cur.fetchall())
    conn.close()
    return template("message_detail.html", q=question, replies=replies, ident=ident)


@post('/insert_reply')
def insert_reply():
    author = request.forms['author']
    body = request.forms['body']
    question_id = request.forms['question_id']
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    qbody = """INSERT INTO Replies(author,body,time,question_id) 
               VALUES (:author, :body, CURRENT_TIMESTAMP, :question_id)"""
    params = {'author': author, 'body': body, 'question_id': question_id}
    cur.execute(qbody, params)
    conn.commit()
    conn.close()
    return "Contestación insertada con éxito"
    

@get('/search_question')
def search_question():
    tag = request.query['tag']
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    qbody = """SELECT id,author,title,time,tags 
               FROM Questions 
               WHERE tags LIKE :pattern
               ORDER BY time DESC"""
    params = {'pattern': '%' + tag + '%'}
    cur.execute(qbody,params)
    res = list(cur.fetchall())
    conn.close()
    return template('messages_search.html', questions=res, tag=tag)

    
if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)
