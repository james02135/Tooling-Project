import pytest
from tooling_project import app
from flask_login import login_user


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "this_should_be_secret"
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client
