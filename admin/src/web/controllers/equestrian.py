from flask import Blueprint
from flask import render_template
from flask import request,redirect, flash,url_for

from flask import session
from src.core import equestrian

bp=Blueprint("ecuestre",__name__,url_prefix="/ecuestre")

@bp.get("/")
def index():
    return render_template("ecuestre/index.html", horses=equestrian.list_horses())

@bp.get("/<int:id>")
def show(id: int):
    """Detalle de un caballo en específico"""
    horse = equestrian.get_horse_by_id(id)
    return render_template('ecuestre/show.html', horse=horse)

@bp.route("/create", methods=['GET', 'POST'])
def create():
    return render_template('ecuestre/create.html', activities=equestrian.list_activities())