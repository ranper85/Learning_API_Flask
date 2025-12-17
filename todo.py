
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def init_db():
  with sqlite3.connect('todo.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS todos(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      completed BOOLEAN NOT NULL CHECK (completed IN (0,1))
                      )''')
    conn.commit()

init_db()

def insert_todo(title, completed):
  with sqlite3.connect('todo.db') as conn:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todos (title, completed) VALUES (?, ?)', (title, completed)) 
    conn.commit()
    return [{'id': cursor.lastrowid, 'title': title, 'completed': completed}]

def select_todo(id = None):
  sql = None
  if id == None:
    sql = 'SELECT * FROM todos WHERE completed = 0'
  elif id > 0:
    sql = 'SELECT * FROM todos WHERE id = ' + str(id)
  with sqlite3.connect('todo.db') as conn:
    cursor = conn.cursor()
    cursor.execute(sql)
    todos = cursor.fetchall()
    todo_list = [ {'id': row[0], 'title': row[1], 'completed': bool(row[2]) } for row in todos ] 
  return todo_list

# POST /todo - lägga till en uppgift
@app.route('/todo', methods=['POST'])
def create_todo():
  data = request.get_json()
  title = data.get('title')
  return insert_todo(title, False), 201

# GET /todo - hämta alla uppgifter
@app.route('/todo', methods=['GET'])
def get_todos():
  return jsonify(select_todo()), 200

# GET /todo/1 - hämtar en specifik uppgift
@app.route('/todo/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
  return jsonify(select_todo(todo_id)), 200

# PUT /todo/1 - markera som klar
@app.route('/todo/<int:todo_id>', methods=['PUT'])
def mark_completed(todo_id):
  with sqlite3.connect('todo.db') as conn:
    cursor = conn.cursor()
    cursor.execute('UPDATE todos SET completed = ? WHERE id = ?', (True, todo_id))
    conn.commit()
  return jsonify({'id': todo_id, 'completed': True}), 200

# DELETE /todo/1 - radera en uppgift
@app.route('/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  with sqlite3.connect('todo.db') as conn:
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', str(todo_id))
    conn.commit()
  return jsonify({'message': 'Task deleted', 'id': todo_id}), 200




if __name__ == '__main__':
  app.run(debug=True)



