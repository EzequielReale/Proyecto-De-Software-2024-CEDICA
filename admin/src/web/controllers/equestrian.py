from datetime import datetime

from flask import (
    Blueprint,
    flash,
    json,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from src.core import equestrian, people
from src.core.database import db
from src.web.handlers.autenticacion import check_permission, login_required
from src.web.handlers.error import unauthorized

bp=Blueprint("ecuestre",__name__,url_prefix="/ecuestre")

@bp.get("/")
@login_required
def index():
    order_by = request.args.get('order_by', 'name')
    order = request.args.get('order', 'asc')
    limit = int(request.args.get('limit', 10))
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    activity_id = request.args.get('activity_id', type=int)
    
    horses, total_pages = equestrian.list_horses(order_by=order_by, order=order, limit=limit, page=page, search=search, activity_id=activity_id)
    
    return render_template("ecuestre/index.html", horses=horses, activities=equestrian.list_activities(), order_by=order_by, order=order, limit=limit, page=page, search=search, activity_id=activity_id, total_pages=total_pages)

@bp.get("/<int:id>")
@login_required
def show(id: int):
    """Detalle de un caballo en específico"""
    horse = equestrian.get_horse_by_id(id)
    return render_template('ecuestre/show.html', horse=horse)

@bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    return render_template('ecuestre/create.html', activities=equestrian.list_activities(), members=people.list_members())

@bp.post("/<int:id>/delete")
@login_required
def destroy(id: int):
    """Eliminar un caballo de la institución"""
    horse = equestrian.horse_delete(id)
    return redirect(url_for('ecuestre.index'))


@bp.route('/<int:id>/add_document', methods=['POST'])
def upload(id: int):
    """Recibe el ID de un caballo y agrega un documento a su lista de documentos"""
    if 'file' not in request.files:
        equestrian.horse_attach_document(id, request.form['doc-type'], request.form['doc-url'], request.form['doc-name'])
    else:
        equestrian.horse_add_document(id, request.form['doc-type'], request.files['file'])
    
    flash(f"Documento agregado exitosamente", "success")
    return redirect(url_for('ecuestre.show', id=id, initial_page=1))


@bp.post("/<int:id>/delete_document/<int:document_id>")
def delete_document(id: int, document_id: int)->str:
    """Recibe el ID de un caballo y el ID de un documento y lo elimina de la BD"""
    equestrian.delete_document(document_id)
    flash(f"Documento eliminado exitosamente", "success")
    return redirect(url_for('ecuestre.show', id=id, initial_page=1))


def validate_horse_form(data):
    errors = []

    # Validar nombre
    if not data.get('name') or len(data['name']) > 100:
        errors.append("El nombre es obligatorio y debe tener menos de 100 caracteres.")
    
    # Validar fecha de nacimiento
    try:
        datetime.strptime(data['birth_date'], '%Y-%m-%d')
    except ValueError:
        errors.append("La fecha de nacimiento es obligatoria y debe tener el formato YYYY-MM-DD.")
    
    # Validar fecha de entrada
    try:
        datetime.strptime(data['entry_date'], '%Y-%m-%d')
    except ValueError:
        errors.append("La fecha de entrada es obligatoria y debe tener el formato YYYY-MM-DD.")
        
    # Validar que la fecha de nacimiento sea anterior a la fecha de entrada
    if data['birth_date'] >= data['entry_date']:
        errors.append("La fecha de nacimiento debe ser anterior a la fecha de entrada.")
    
    # Validar género
    if data.get('gender') not in ['0', '1']:
        errors.append("El género es obligatorio y debe ser Macho o Hembra.")
    
    # Validar origen
    if data.get('origin') not in ['0', '1']:
        errors.append("El origen es obligatorio y debe ser Compra o Donación.")
    
    # Validar raza
    if not data.get('race') or len(data['race']) > 100:
        errors.append("La raza es obligatoria y debe tener menos de 100 caracteres.")
    
    # Validar pelaje
    if not data.get('coat') or len(data['coat']) > 100:
        errors.append("El pelaje es obligatorio y debe tener menos de 100 caracteres.")
    
    # Validar ubicación asignada
    if not data.get('assigned_location') or len(data['assigned_location']) > 100:
        errors.append("La ubicación asignada es obligatoria y debe tener menos de 100 caracteres.")

    return errors
