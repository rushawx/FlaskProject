import datetime
import secrets

from flask import (
    Flask,
    flash,
    render_template,
    request,
    session,
    abort,
    redirect,
    url_for,
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = datetime.timedelta(minutes=30)


@app.route("/", methods=["GET"])
def index():
    if "username" in session:
        return f"""
        Logged in as {session["username"]}
        <br>
        <a href="/logout">Logout</a>
        """
    abort(401)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session.permanent = True
        return redirect(url_for("index"))
    return """
    <form method="post">
        <label>Name:
        <p><input type=text name=username>
        <p><input type=submit value=Login>
    </form>
    """


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.errorhandler(401)
def error401(e):
    return """
    <h2>You are not logged in<h2>
    <a href="/login">Login</a>
    """


@app.route("/calculate", methods=["POST"])
def calculate():
    number1 = request.form["number1"]
    number2 = request.form["number2"]

    if number1.isdigit() and number2.isdigit():
        number1 = int(number1)
        number2 = int(number2)

        operation = request.form["operation"]

        if operation == "add":
            output = number1 + number2
            flash(f"Результат: {output}")
        elif operation == "multiply":
            output = number1 * number2
            flash(f"Результат: {output}")
        elif operation == "power":
            output = number1**number2
            flash(f"Результат: {output}")
        elif operation == "divide":
            if number2 != 0:
                output = number1 / number2
                flash(f"Результат: {output}")
            else:
                flash("Ошибка: деление на ноль!")

    else:
        flash("Ошибка, введите корректные числа")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
