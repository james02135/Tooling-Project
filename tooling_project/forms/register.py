from flask import request, render_template
from forms import RegisterForm
import hashlib
import psycopg2


class Register:

    temp_name = request.form.get("name", "")
    temp_ID = request.form.get("ID", "")
    temp_email = request.form.get("email", "")
    temp_password = request.form.get(
        "password",
    )
    n_message = "Please fill in your name"

    # check for blanks
    if temp_name == "":
        return render_template("forms/register.html", message=n_message)
    else:
        name = temp_name

    if temp_ID == "":
        i_message = "Please fill in your Student ID Number"
        return render_template("forms/register.html", message=i_message)
    else:
        ID = temp_ID

    if temp_email == "":
        e_message = "Please fill in your email address"
        return render_template("forms/register.html", message=e_message)
    else:
        email = temp_email

    if temp_password == "":
        p_message = "Please fill in your password"
        return render_template("register.html", message=p_message)
    else:
        p_hashed = hashlib.sha256(
            temp_password.encode()
        )  # hash the password the user entered
        hashed_password = p_hashed.hexdigest()

    # database insert
    host = "postgresql:///intool"
    port = "5432"
    dbname = "intool"
    user = "james"
    pw = ""
    db_conn = psycopg2.connect(
        host=host, port=port, dbname=dbname, user=user, password=pw
    )
    db_cursor = db_conn.cursor()

    # We take the time to build our SQL query string so that
    #   (a) we can easily & quickly read it
    #   (b) we can easily & quickly edit or add/remote lines
    #   The more complex the query, the greater the benefits
    s = "INSERT INTO intool.users "
    s += "("
    s += "  name"
    s += "  ID"
    s += "  email"
    s += ", hashed_password"
    s += ") VALUES ("
    s += " '" + name + "'"
    s += " '" + ID + "'"
    s += " '" + email + "'"
    s += ",'" + hashed_password + "'"
    s += ")"
    db_cursor.execute(s)
    try:
        db_conn.commit()
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n SQL: " + s
        return render_template("register.html", message=t_message)

    t_message = "Your user account has been added."
    return render_template("register.html", message=t_message)
