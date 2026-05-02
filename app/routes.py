from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify
from .db import get_db

bp = Blueprint("main", __name__)


def get_task(task_id):
    db = get_db()
    task = db.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        abort(404)

    return task


@bp.route("/")
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


@bp.route("/add", methods=["POST"])
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

    return redirect(url_for("main.index"))


@bp.route("/tasks/<int:id>/delete", methods=["POST"])
def delete_task(id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("main.index"))


@bp.route("/tasks/<int:id>/edit", methods=["GET", "POST"])
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
            return redirect(url_for("main.index"))

    return render_template("edit_task.html", task=task)


@bp.route("/tasks/<int:id>/move", methods=["POST"])
def move_task(id):
    task = get_task(id)
    new_status = request.json.get("status")

    if new_status not in ["todo", "in_progress", "done"]:
        return jsonify({"success": False, "message": "Invalid status"}), 400

    db = get_db()
    db.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (new_status, id)
    )
    db.commit()

    return jsonify({"success": True})