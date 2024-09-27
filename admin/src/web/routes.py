from flask import render_template


def register(app):
    @app.route("/", endpoint="home")
    def home(): 
        return render_template("home.html")
    
    @app.route("/jya", endpoint="jya")
    def jya(): 
        return render_template("jya/index.html")
        
    @app.route("/ecuestre", endpoint="ecuestre")
    def ecuestre(): 
        return render_template("ecuestre/index.html")
        
    @app.route("/team", endpoint="team")
    def team(): 
        return render_template("team/index.html")