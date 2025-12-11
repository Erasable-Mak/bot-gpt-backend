import pytest
import os
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    os.environ["LLM_PROVIDER"] = "stub"
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
    with app.app_context():
        db.create_all()
        user = User(username="alice")
        db.session.add(user)
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_create_conversation(client):
    resp = client.post("/api/conversations", json={"user_id": 1, "message": "Hello"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["id"]
    assert data["messages"][0]["content"] == "Hello"
