import sqlite3
import click
from flask import Flask, render_template, request, redirect, url_for, g, abort

app = Flask(__name__)
app.config["DATABASE"] = "database.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


@app.cli.command("init-db")
def init_db_command():
    """Создаёт таблицы базы данных."""
    init_db()
    click.echo("Database initialized.")

def get_task(task_id):
    db = get_db()
    task = db.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        abort(404)

    return task

@app.route("/")
def index():
    db = get_db()

    todo_tasks = db.execute(
        "SELECT * FROM tasks WHERE status = ?",
        ("todo",)
    ).fetchall()

    in_progress_tasks = db.execute(
        "SELECT * FROM tasks WHERE status = ?",
        ("in_progress",)
    ).fetchall()

    done_tasks = db.execute(
        "SELECT * FROM tasks WHERE status = ?",
        ("done",)
    ).fetchall()

    return render_template(
        "index.html",
        todo_tasks=todo_tasks,
        in_progress_tasks=in_progress_tasks,
        done_tasks=done_tasks
    )

@app.route("/tasks/<int:id>/delete", methods=["POST"])
def delete_task(id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("index"))

@app.route("/tasks/<int:id>/edit", methods=["GET", "POST"])
def edit_task(id):
    task = get_task(id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "todo")

        if title:
            db = get_db()
            db.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, status = ?
                WHERE id = ?
                """,
                (title, description, status, id)
            )
            db.commit()
            return redirect(url_for("index"))

    return render_template("edit_task.html", task=task)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    status = request.form.get("status", "todo")

    if title:
        db = get_db()
        db.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
            (title, description, status)
        )
        db.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)