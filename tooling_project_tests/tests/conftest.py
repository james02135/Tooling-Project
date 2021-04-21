import pytest
from tooling_project import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config["SECRET_KEY"] = 'this_should_be_secret'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


@pytest.fixture
def dummy_user():
    id = '11111111'
    name = 'Dummy'
    email = 'dummy@example.com'
    password = 'dummy_password'
    github_username = 'dummy'
    github_token = 'dummy'
    yield 