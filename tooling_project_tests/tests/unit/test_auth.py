import pytest
from bs4 import BeautifulSoup
from tooling_project.auth import *
from tooling_project_tests.tests.conftest import client


# Test the register route
def test_register(client):
    result = client.get("/register")
    assert result.status_code == 200
    page = BeautifulSoup(result.data, "html.parser")
    assert page.title
    assert page.title.string == "Register"


# Test register post
def test_register_post(client):
    result = client.post(
        "/register",
        data=dict(
            id="11111111",
            name="Dummy",
            email="dummy@example.com",
            password="dummy_password",
            github_username="dummy",
            github_token="dummy_token",
        ),
        follow_redirects=True,
    )
    print(result.data)
    page = BeautifulSoup(result.data, "html.parser")
    assert page.title
    assert page.title.string == "Register"


# Test the login route
def test_login(client):
    result = client.get("/login")
    assert result.status_code == 200
    page = BeautifulSoup(result.data, "html.parser")
    assert page.title
    assert page.title.string == "Login"


# Test a login
def test_login_post(client):
    result = client.post(
        "/login",
        data=dict(email="dummy@example.com", password="dummy_password"),
        follow_redirects=True,
    )
    print(result.data)
    page = BeautifulSoup(result.data, "html.parser")
    assert page.title
    assert page.title.string == "Dashboard"


# Test the menu route
def test_menu_redirecting(client):
    result = client.get("/menu")
    assert result.status_code == 302
    page = BeautifulSoup(result.data, "html.parser")
    assert page.title
    assert page.title.string == "Redirecting..."


def test_logout(client):
    result = client.get("/logout", follow_redirects=False)
    assert result.status_code == 302
    assert result.location == "http://localhost/login?next=%2Flogout"
    assert "noggin_session" not in session
    assert "noggin_username" not in session
    assert "noggin_ipa_server_hostname" not in session
