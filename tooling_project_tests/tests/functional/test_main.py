import pytest
from tooling_project import app
from tooling_project.main import *
from bs4 import BeautifulSoup
from tooling_project_tests.tests.conftest import client


#Test the home route
def test_home(client):
    result = client.get('/')
    assert result.status_code == 200
    page = BeautifulSoup(result.data, 'html.parser')
    assert page.title
    assert page.title.string == 'Home'


# Test the about route
def test_about(client):
    result = client.get('/about')
    assert result.status_code == 200
    page = BeautifulSoup(result.data, 'html.parser')
    assert page.title
    assert page.title.string == 'About'


# Test the tutorial route
def test_tutorial(client):
    result = client.get('/tutorial')
    assert result.status_code == 200
    page = BeautifulSoup(result.data, 'html.parser')
    assert page.title
    assert page.title.string == 'Tutorial'


# Test the dashboard route is finding (302) and redirecting
def test_dashboard_redirect(client):
    result = client.get('/dashboard')
    assert result.status_code == 302
    page = BeautifulSoup(result.data, 'html.parser')
    assert page.title
    assert page.title.string == 'Redirecting...'