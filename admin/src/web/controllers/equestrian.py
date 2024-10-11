from flask import Blueprint
from flask import request
from flask import render_template
from flask import request,redirect
from flask import session
from flask import url_for
from flask import json
from flask import flash
from src.core.database import db
from src.web.handlers.autenticacion import check_permission,login_required
from src.web.handlers.error import unauthorized
from src.core import equestrian
from src.core import people

bp=Blueprint("ecuestre",__name__,url_prefix="/ecuestre")

@bp.get("/")
@login_required
def index():
    if  not check_permission(session,"encuestre_index"):
         return unauthorized()
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
    if  not check_permission(session,"encuestre_show"):
         return unauthorized()
    order_by = request.args.get('order_by', 'document_type_id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search', '')
    initial_page = request.args.get('initial_page', 0, type=int)
    document_type_id = request.args.get('document_type_id', type=int)
        
    horse = equestrian.get_horse_by_id(id)
    return render_template('ecuestre/show.html', horse=horse, document_type_id=document_type_id, order_by=order_by, order=order, search=search, initial_page=1 if document_type_id else initial_page, document_types=equestrian.get_document_types(), documents=equestrian.get_horse_documents(id, document_type_id=document_type_id, search=search, order_by=order_by, order=order))

@bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if  not check_permission(session,"encuestre_new"):
         return unauthorized()
    # Si se envía el formulario
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
        
        flash(f"Caballo creado exitosamente", "success")
        return redirect(url_for('ecuestre.index'))
    
    return render_template('ecuestre/create.html', activities=equestrian.list_activities(), drivers=equestrian.get_drivers(), trainers=equestrian.get_trainers())

@bp.route("/<int:id>/update", methods=['GET', 'POST'])
def update(id: int)->str:
    """Recibe el id de un caballo y muestra el formulario para editarlo, o lo actualiza en caso de que se envíe el formulario"""
    if  not check_permission(session,"encuestre_update"):
         return unauthorized()
    horse = equestrian.get_horse_by_id(id)

    # Convertir el objeto horse a un diccionario
    horse_dict = {
        'id': horse.id,
        'name': horse.name,
        'birth_date': horse.birth_date.strftime('%Y-%m-%d'),
        'entry_date': horse.entry_date.strftime('%Y-%m-%d'),
        'gender': horse.gender,
        'donation': horse.donation,
        'race': horse.race,
        'coat': horse.coat,
        'assigned_location': horse.assigned_location,
        'activities': [{'id': activity.id, 'name': activity.name} for activity in horse.activities],
        'members': [{'id': member.id, 'name': member.name, 'job': member.job.name} for member in horse.assigned_members]
    }
    
    # Si se envía el formulario
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
            
        # Editar el caballo
        equestrian.horse_update(
            horse.id,
            name=name,
            birth_date=birth_date,
            entry_date=entry_date,
            gender="Macho" if gender == 0 else "Hembra",
            donation=origin == 1,
            race=race,
            coat=coat,
            assigned_location=assigned_location,
            activities=selected_activities,
            members=assigned_members
        )
        
        flash(f"Caballo actualizado exitosamente", "success")
        return redirect(url_for('ecuestre.index'))
    
    return render_template('ecuestre/update.html', horse=horse_dict, activities=equestrian.list_activities(), drivers=equestrian.get_drivers(), trainers=equestrian.get_trainers())


@bp.post("/<int:id>/delete")
@login_required
def destroy(id: int):
    """Eliminar un caballo de la institución"""
    if  not check_permission(session,"encuestre_destroy"):
         return unauthorized()
    horse = equestrian.horse_delete(id)
    flash(f"Caballo {horse.name} eliminado exitosamente", "success")
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