import pytest
from bs4 import BeautifulSoup
from tooling_project.auth import *
from tooling_project_tests.tests.conftest import client, dummy_user


# Test the register route
def test_register(client):
    result = client.get('/register')
    assert result.status_code == 200
    page = BeautifulSoup(result.data, 'html.parser')
    assert page.title
    assert page.title.string == 'Register'

# def test_register_post():

# Test the login route
def test_login(client):
    result = client.get('/login')
    assert result.status_code == 200
    page = BeautifulSoup(result.data, 'html.parser')
    assert page.title
    assert page.title.string == 'Login'


# Test a login
def test_login_post(client, dummy_user):
    result = client.post(
        '/login',
        data={
            "email": "Dummy",
            "password": "dummy_password",
        },
        follow_redirects=True,
    )
    print(result.data)
    page = BeautifulSoup(result.data, 'html.parser')
    assert page.title
    assert page.title.string == 'Login'
    
    
# Test the menu route
def test_menu_redirecting(client):
    result = client.get('/menu')
    assert result.status_code == 302
    page = BeautifulSoup(result.data, 'html.parser')
    assert page.title
    assert page.title.string == 'Redirecting...'

# def test_menu_post():

# def test_logout():
