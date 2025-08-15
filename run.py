from db import get_connection


from flask import Flask, request, render_template
app=Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")


from flask import redirect, url_for


@app.route("/delete-user/<int:id>")
def delete_user(id):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s",(id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("users"))


@app.route("/edit-user/<int:id>")
def edit_user_form(id):
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user=cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template("edit_user_form.html", user=user)


@app.route("/update-user/<int:id>",methods=["POST"])
def update_user(id):
    name=request.form["name"]
    email=request.form["email"]

    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (name, email, id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for("users"))




@app.route("/add-user", methods=["POST"])
def add_user():
    name=request.form["name"]
    email=request.form["email"]
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        "INSERT INTO users (name,email) VALUES(%s,%s)",
        (name,email)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return f"User {name} added!"

@app.route("/add-application",methods=["POST"])
def add_application():
    company=request.form["company"]
    position=request.form["position"]
    status=request.form["status"]
    deadline=request.form["deadline"]
    notes=request.form["notes"]

    user_id=1


    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        "INSERT INTO applications(user_id,company,position,status,deadline,notes) VALUES(%s,%s,%s,%s,%s,%s)",
        (user_id,company,position, status, deadline, notes)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return f"Internship application for {position} at {company} added!"


@app.route("/add-application-form")
def add_application_form():
    return render_template("add_application_form.html")

@app.route("/applications")
def view_applications():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM applications")
    rows=cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("applications.html", applications=rows)


@app.route("/delete-application/<int:id>", methods=["POST"])
def delete_application(id):
    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute("DELETE FROM applications WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return f"Deleted application {id}. <a href='/applications'>Go back</a>"


@app.route("/edit-application/<int:id>")
def edit_application_form(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM applications WHERE id = %s", (id,))
    app_data = cursor.fetchone()
    cursor.close()
    connection.close()

    if app_data:
        return render_template("edit_application_form.html", app=app_data)
    else:
        return f"No application found with ID {id}"


@app.route("/update-application/<int:id>", methods=["POST"])
def update_application(id):
    company = request.form["company"]
    position = request.form["position"]
    status = request.form["status"]
    deadline = request.form["deadline"]
    notes = request.form["notes"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE applications SET company=%s, position=%s, status=%s, deadline=%s, notes=%s WHERE id=%s",
        (company, position, status, deadline, notes, id)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return f"Updated application {id}. <a href='/applications'>Go back</a>"




@app.route("/users")
def users():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("users.html", users=rows)


@app.route("/add-user-form")
def add_user_form():
    return render_template("add_user_form.html")


if __name__=="__main__":
    app.run(debug=True)
