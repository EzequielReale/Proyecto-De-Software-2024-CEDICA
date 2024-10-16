from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.core.user_role_permission.operations.user_operations import (
    find_user,
    get_roles_from_user,
    get_user_by_email,
)


bp= Blueprint("auth",__name__,url_prefix="/auth")


@bp.get("/")
def login():
    return render_template("auth/login.html")

@bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
    else:
        flash("No se encontro ninguna sesion activa","error")
    return redirect(url_for("auth.login"))


@bp.post("/authenticate")
def authenticate():
   """me fijo si el usuario esta registrado, si lo esta le doy acceso de lo contrario le mustro msj de error"""
   parametros = request.form
   user = find_user(parametros["email"],parametros["password"])
   if not user:
       flash("Usuario o contraseña incorrecta", "error")
       return redirect(url_for("auth.login"))
   if user.isActive == False:
       flash("Usuario bloqueado", "error")
       return redirect(url_for("auth.login"))
   session["user"] = user.email
   flash("La sesion se inicio correctamente!", "success")
   return render_template("home.html")


@bp.get("/profile")
def profile():
    if session.get("user"):
        return render_template("auth/profile.html", user=session["user"], roles=get_roles_from_user(session["user"]), user_alias=get_user_by_email(session["user"]).alias)
    else:
        flash("Usted no se encuentra autenticado","error")
        return redirect(url_for("auth.login"))
