from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        age = request.form.get("age")
        city = request.form.get("city")
        language = request.form.get("language")
        return render_template("result.html", name=username, age=age, city=city, language=language)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
