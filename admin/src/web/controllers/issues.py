from flask import render_template
from flask import Blueprint

from src.core import board


bp = Blueprint("issues", __name__, url_prefix ="/consultas") 

@bp.get("/")
# Listado de issues
def index():
    issues = board.list_issues()

   # Tomo los datos de la bd y renderizo la pagina mandandole esos datos
    
    return render_template('issues/index.html',issues=issues)