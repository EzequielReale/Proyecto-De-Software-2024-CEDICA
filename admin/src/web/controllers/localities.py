from flask import Blueprint, jsonify

from src.core import adressing
from src.web.handlers.autenticacion import login_required


bp = Blueprint("localities", __name__, url_prefix ="/localities") 

@bp.route('/get/<province_id>')
@login_required
def get_localities(province_id):
    localities = adressing.get_localities_by_province(province_id)
    localities_list = [{'id': loc.id, 'name': loc.name} for loc in localities]
    return jsonify(localities_list)
