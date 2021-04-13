from tooling_project.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User(
        '87654321',
        "Pat Kenny",
        "patkennedy79@gmail.com",
        "FlaskIsAwesome",
        "patkenny2021",
        "None",
    )
    assert user.id == '87654321'
    assert user.name == "Pat Kenny"
    assert user.email == "patkennedy79@gmail.com"
    assert user.password == 'FlaskIsAwesome'
    assert user.github_username == "patkenny2021"
    assert user.github_token == "None"
