from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = [
    {
        "title": "Тестовая карточка 1",
        "description": "Тестовое описание 1.",
        "status": "todo"
    },
    {
        "title": "Тестовая карточка 2",
        "description": "Тестовое описание 2.",
        "status": "todo"
    },
    {
        "title": "Тестовая задача 3",
        "description": "Тестовое описание 3.",
        "status": "in_progress"
    },
    {
        "title": "Тестовая задача 4",
        "description": "Тестовое описание 4.",
        "status": "done"
    }
]

@app.route("/", methods=["GET"])
def index():
    todo_tasks = [task for task in tasks if task["status"] == "todo"]
    in_progress_tasks = [task for task in tasks if task["status"] == "in_progress"]
    done_tasks = [task for task in tasks if task["status"] == "done"]

    return render_template(
        "index.html",
        todo_tasks=todo_tasks,
        in_progress_tasks=in_progress_tasks,
        done_tasks=done_tasks
    )

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    status = request.form.get("status", "todo")

    if title:
        tasks.append({
            "title": title,
            "description": description,
            "status": status
        })

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)