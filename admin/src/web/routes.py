from flask import render_template


def register(app):
    @app.route("/", endpoint="home")
    def home(): 
        return render_template("home.html")