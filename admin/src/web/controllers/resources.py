import traceback

from flask import Blueprint, jsonify, flash, redirect, url_for

from src.core import adressing, database, disabilities, seeds as seed_db
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


@bp.route('/seeds')
@login_required
def seeds():
    """ Ejecuta los seeds para crear registros en la BD"""
    try:
        database.reset()
        seed_db.run()
        flash("Se reinicio la BD y se ejecutaron los seeds con exito", "success")
    except Exception as e:
        error_message = f"Error al ejecutar los seeds: {e}. Intente nuevamente"
        error_traceback = traceback.format_exc()
        flash(f"{error_message}\n{error_traceback}", "danger")

    return redirect(url_for('home'))
