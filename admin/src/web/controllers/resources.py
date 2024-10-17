from flask import Blueprint, jsonify

from src.core import adressing, disabilities
from src.web.handlers.autenticacion import login_required


bp = Blueprint("resources", __name__, url_prefix ="/resources") 


@bp.route('/localities/<int:province_id>')
@login_required
def get_localities(province_id):
    localities = adressing.get_localities_by_province(province_id)
    localities_list = [{'id': loc.id, 'name': loc.name} for loc in localities]
    return jsonify(localities_list)


@bp.route('/disabilities/<int:type_id>')
@login_required
def get_disabilities(type_id):
    disabilities_list = disabilities.get_diagnosis_by_type(type_id)
    disabilities_dict = [{'id': dis.id, 'name': dis.name} for dis in disabilities_list]
    return jsonify(disabilities_dict)
