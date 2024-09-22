from flask import Blueprint
from flask import render_template
from flask import request,redirect, flash,url_for

from flask import session
from src.core import auth

bp= Blueprint("auth",__name__,url_prefix="/auth")

@bp.get("/")
def login():
    return render_template("auth/login.html")

@bp.get("/logout")
def logout():
    pass

@bp.post("/authenticate")
def authenticate():
   """me fijo si el usuario esta registrado, si lo esta le doy acceso de lo contrario le mustro msj de error"""
   parametros = request.form
   user = auth.find_user(parametros["email"],parametros["password"])
   if not user:
       flash("Usuario o contraseña incorrecta", "error")
       return redirect(url_for("auth.login"))
   session["user"] = user.email
   flash("La sesion se inicio correctamente!", "success")
   return render_template("layout.html")