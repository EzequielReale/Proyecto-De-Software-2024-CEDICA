from flask import Blueprint
from flask import request
from flask import jsonify
from flask import render_template
from flask import request,redirect
from flask import url_for
from flask import current_app
from flask import json
from src.core.database import db
from src.web.handlers.autenticacion import login_required
from src.core import equestrian
from src.core import people
from werkzeug.utils import secure_filename
from os import fstat

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
    return render_template('ecuestre/show.html', horse=horse, document_types=equestrian.get_document_types(), documents=equestrian.get_horse_documents(id))

@bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form['name']
        birth_date = request.form['birth_date']
        entry_date = request.form['entry_date']
        gender = request.form['gender']
        origin = request.form['origin']
        race = request.form['race']
        coat = request.form['coat']
        assigned_location = request.form['assigned_location']
        
        # Obtener las actividades seleccionadas
        selected_activities = request.form.get('selected_activities')
        if selected_activities:
            selected_activities = json.loads(selected_activities)
        else:
            selected_activities = []
            
        # Obtener los miembros asignados
        assigned_members = request.form.get('assigned_members')
        if assigned_members:
            assigned_members = json.loads(assigned_members)
        else:
            assigned_members = []
            
        # Crear el caballo
        horse = equestrian.horse_new(
            name=name,
            birth_date=birth_date,
            entry_date=entry_date,
            gender="Macho" if gender == 0 else "Hembra",
            donation=origin == 1,
            race=race,
            coat=coat,
            assigned_location=assigned_location
        )    

        # Asignar actividades al caballo
        for activity_id in selected_activities:
            activity = equestrian.get_activity_by_id(activity_id)
            if activity:
                horse.activities.append(activity)
        
        # Asignar miembros al caballo
        for member_id in assigned_members:
            member = people.get_member_by_field('id', member_id)
            if member:
                horse.assigned_members.append(member)

        
        db.session.commit()
        
        return redirect(url_for('ecuestre.index'))
    
    return render_template('ecuestre/create.html', activities=equestrian.list_activities(), drivers=equestrian.get_drivers(), trainers=equestrian.get_trainers())

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
        equestrian.horse_attach_document(id, request.form['doc-type'], request.form['document-url'])
    else:
        equestrian.horse_add_document(id, request.form['doc-type'], request.files['file'])
        
    return redirect(url_for('ecuestre.show', id=id))
