import sqlite3
from flask import Flask, request

app = Flask(__name__)

def db():
    con = sqlite3.connect("tasks.db")
    con.row_factory = sqlite3.Row
    con.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)")
    return con

def as_dict(r):
    return {"id": r["id"], "title": r["title"], "done": bool(r["done"])}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    with db() as con:
        tasks = [as_dict(r) for r in con.execute("SELECT * FROM tasks")]
    done = request.args.get("done")
    if done is not None:
        tasks = [t for t in tasks if t["done"] == (done == "true")]
    return tasks

@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        return {"error": "title is required"}, 400
    with db() as con:
        cur = con.execute("INSERT INTO tasks (title) VALUES (?)", (data["title"],))
    task = {"id": cur.lastrowid, "title": data["title"], "done": False}
    return task, 201, {"Location": f"/tasks/{task['id']}"}

@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    with db() as con:
        r = con.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return as_dict(r) if r else ({"error": "not found"}, 404)

@app.put("/tasks/<int:task_id>")
def replace_task(task_id):
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        return {"error": "title is required"}, 400
    with db() as con:
        cur = con.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?",
                          (data["title"], int(bool(data.get("done"))), task_id))
    if cur.rowcount == 0:
        return {"error": "not found"}, 404
    return {"id": task_id, "title": data["title"], "done": bool(data.get("done"))}

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    with db() as con:
        cur = con.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return ("", 204) if cur.rowcount else ({"error": "not found"}, 404)

@app.get("/tasks/count")
def count_tasks():
    with db() as con:
        n = con.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    return {"count": n}
