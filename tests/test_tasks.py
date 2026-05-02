from app.db import get_db


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add_task(client, app):
    response = client.post("/add", data={
        "title": "Тестовая задача",
        "description": "Описание тестовой задачи",
        "status": "todo"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Тестовая задача".encode("utf-8") in response.data

    with app.app_context():
        db = get_db()
        task = db.execute(
            "SELECT * FROM tasks WHERE title = ?",
            ("Тестовая задача",)
        ).fetchone()
        assert task is not None


def test_edit_task(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
            ("Старая задача", "Старое описание", "todo")
        )
        db.commit()

        task = db.execute(
            "SELECT * FROM tasks WHERE title = ?",
            ("Старая задача",)
        ).fetchone()

    response = client.post(f"/tasks/{task['id']}/edit", data={
        "title": "Новая задача",
        "description": "Новое описание",
        "status": "done"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Новая задача".encode("utf-8") in response.data

    with app.app_context():
        db = get_db()
        updated_task = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task["id"],)
        ).fetchone()

        assert updated_task["title"] == "Новая задача"
        assert updated_task["description"] == "Новое описание"
        assert updated_task["status"] == "done"


def test_delete_task(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
            ("Удаляемая задача", "Описание", "todo")
        )
        db.commit()

        task = db.execute(
            "SELECT * FROM tasks WHERE title = ?",
            ("Удаляемая задача",)
        ).fetchone()

    response = client.post(
        f"/tasks/{task['id']}/delete",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        deleted_task = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task["id"],)
        ).fetchone()

        assert deleted_task is None


def test_init_db_command(runner):
    result = runner.invoke(args=["init-db"])
    assert result.exit_code == 0
    assert "Database initialized." in result.output