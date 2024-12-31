from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# initilialize database
def init_db():
    conn = sqlite3.connect('todo.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
    print("Table created successfully")
    conn.close()


# home page : displays all tasks
@app.route('/', methods=['GET'])
def index():
    with sqlite3.connect("todo.db") as conn:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
    return render_template("index.html", tasks=tasks)

# add a new task
@app.route('/add', methods=['POST'])
def add():
    with sqlite3.connect("todo.db") as conn:
        content = request.form['task']
        conn.execute("INSERT INTO tasks (content) VALUES (?)", (content,))
        conn.commit()
    return redirect(url_for("index"))

# delete a task
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id: int):
    with sqlite3.connect("todo.db") as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)