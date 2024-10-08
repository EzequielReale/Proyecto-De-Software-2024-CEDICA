from flask import Blueprint, jsonify

from src.core import adressing


bp = Blueprint("localities", __name__, url_prefix ="/localities") 

@bp.route('/get/<province_id>')
def get_localities(province_id):
    localities = adressing.get_localities_by_province(province_id)
    localities_list = [{'id': loc.id, 'name': loc.name} for loc in localities]
    return jsonify(localities_list)
