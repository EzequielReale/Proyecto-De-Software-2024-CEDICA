from flask import render_template
from flask import Blueprint

from src.core import people


bp = Blueprint("team", __name__, url_prefix ="/team") 

@bp.get("/")
def index():
    """Listado de miembros del equipo"""
    members = people.list_members()
    return render_template('team/index.html', members=members)
