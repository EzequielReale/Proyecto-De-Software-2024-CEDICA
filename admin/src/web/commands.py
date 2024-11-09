from src.core import database
from src.core import seeds

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.core.user_role_permission.operations.user_operations import (
    find_user,
    get_roles_from_user,
    get_user_by_email,
    user_new,
)


def register(app):
    
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    
    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()
    

    @app.route("/login")
    def google_login():
        redirect_uri = url_for('auth', _external=True)
        print(redirect_uri)  # Debería ser https://127.0.0.1:5000/login/callback
        return app.oauth.google.authorize_redirect(redirect_uri)
    

    
    @app.route('/login/callback')
    def auth():
        token = app.oauth.google.authorize_access_token()
        userinfo = token['userinfo'] 
        
        email = userinfo['email']
        first_name = userinfo['given_name']
        last_name = userinfo['family_name']
        #google_id = userinfo['sub']  # id de Google
        
        user = get_user_by_email(email)
        
        if user is None:
            user = user_new(
                #name=first_name,
                #lastname=last_name, no existe en el modelo
                email=email,
                password="default_password",
            )
         
        else:
            flash("Ya existe un usuario con ese email","error")
            return redirect(url_for("auth.login"))

        flash("Tu registro esta a la espera de la confirmación de un Administrador","info")
        return redirect(url_for("auth.login"))

    