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
from src.core.equestrian.activity import Activity
from src.core.people.member_rider import Member
from src.core.database import db
from src.web.handlers.autenticacion import check_permission, login_required
from src.web.handlers.error import unauthorized

bp=Blueprint("ecuestre",__name__,url_prefix="/ecuestre")

@bp.get("/")
@login_required
def index():
    if  not check_permission(session,"ecuestre_index"):
         return unauthorized()
     
    order_by = request.args.get('order_by', 'name')
    order = request.args.get('order', 'asc')
    limit = int(request.args.get('limit', 12))
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    activity_id = request.args.get('activity_id', type=int)
    
    horses, total_pages = equestrian.list_horses(order_by=order_by, order=order, limit=limit, page=page, search=search, activity_id=activity_id)
    
    return render_template("ecuestre/index.html", horses=horses, activities=equestrian.list_activities(), order_by=order_by, order=order, limit=limit, page=page, search=search, activity_id=activity_id, total_pages=total_pages)

@bp.get("/<int:id>")
@login_required
def show(id: int):
    """Detalle de un caballo en específico"""
    if  not check_permission(session,"ecuestre_show"):
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
    if  not check_permission(session,"ecuestre_new"):
         return unauthorized()
     
    # Si se envía el formulario
    if request.method == 'POST':
        # Obtener los datos del formulario
        form_data = {
            'name': request.form['name'],
            'birth_date': request.form['birth_date'],
            'entry_date': request.form['entry_date'],
            'gender': request.form['gender'],
            'origin': request.form['origin'],
            'race': request.form['race'],
            'coat': request.form['coat'],
            'assigned_location': request.form['assigned_location'],
            'selected_activities': request.form.get('selected_activities'),
            'assigned_members': request.form.get('assigned_members')
        }
        
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
            
        # Validar los datos del formulario
        errors = validate_horse_form(form_data)

        # Si hay errores, mostrar mensajes de error y renderizar el formulario nuevamente
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('ecuestre/create.html', form_data=form_data, activities=equestrian.list_activities(), drivers=equestrian.get_drivers(), trainers=equestrian.get_trainers())
        
        # Crear el caballo
        horse = equestrian.horse_new(
            name=form_data['name'],
            birth_date=form_data['birth_date'],
            entry_date=form_data['entry_date'],
            gender="Macho" if form_data['gender'] == '0' else "Hembra",
            donation=form_data['origin'] == '1',
            race=form_data['race'],
            coat=form_data['coat'],
            assigned_location=form_data['assigned_location']
        ) 
        
        # Verificar y agregar actividades
        if selected_activities:
            for activity_id in selected_activities:
                activity = Activity.query.filter_by(id=activity_id).first()
                if activity:
                    horse.activities.append(activity)
                
        # Verificar y agregar miembros
        if assigned_members:
            for member_id in assigned_members:
                member = Member.query.filter_by(id=member_id).first()
                if member:
                    horse.assigned_members.append(member)
        
        db.session.commit()
        
        flash(f"Caballo creado exitosamente", "success")
        return redirect(url_for('ecuestre.show', id=horse.id))
    
    return render_template('ecuestre/create.html', activities=equestrian.list_activities(), drivers=equestrian.get_drivers(), trainers=equestrian.get_trainers())

@bp.route("/<int:id>/update", methods=['GET', 'POST'])
def update(id: int)->str:
    """Recibe el id de un caballo y muestra el formulario para editarlo, o lo actualiza en caso de que se envíe el formulario"""
    if  not check_permission(session,"ecuestre_update"):
         return unauthorized()
     
    horse = equestrian.get_horse_by_id(id)
    
    if not horse:
        flash(f"El caballo con ID {id} no existe", "danger")
        return redirect(url_for('ecuestre.index'))

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
        form_data = {
            'name': request.form['name'],
            'birth_date': request.form['birth_date'],
            'entry_date': request.form['entry_date'],
            'gender': request.form['gender'],
            'origin': request.form['origin'],
            'race': request.form['race'],
            'coat': request.form['coat'],
            'assigned_location': request.form['assigned_location'],
            'selected_activities': request.form.get('selected_activities'),
            'assigned_members': request.form.get('assigned_members')
        }
        
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
            
        # Validar los datos del formulario
        errors = validate_horse_form(form_data)

        # Si hay errores, mostrar mensajes de error y renderizar el formulario nuevamente
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('ecuestre/update.html', horse=horse_dict, activities=equestrian.list_activities(), drivers=equestrian.get_drivers(), trainers=equestrian.get_trainers())

            
        # Editar el caballo
        equestrian.horse_update(
            horse.id,
            name=form_data['name'],
            birth_date=form_data['birth_date'],
            entry_date=form_data['entry_date'],
            gender="Macho" if form_data['gender'] == 0 else "Hembra",
            donation=form_data['origin'] == 1,
            race=form_data['race'],
            coat=form_data['coat'],
            assigned_location=form_data['assigned_location'],
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
    if  not check_permission(session,"ecuestre_destroy"):
         return unauthorized()
     
    if not equestrian.get_horse_by_id(id):
        flash(f"El caballo con ID {id} no existe", "danger")
        return redirect(url_for('ecuestre.index'))
     
    horse = equestrian.horse_delete(id)
    flash(f"Caballo {horse.name} eliminado exitosamente", "success")
    return redirect(url_for('ecuestre.index'))


@bp.route('/<int:id>/add_document', methods=['POST'])
def upload(id: int):
    """Recibe el ID de un caballo y agrega un documento a su lista de documentos"""
    if not check_permission(session,"ecuestre_update"):
        return unauthorized()
    
    if 'file' not in request.files:
        equestrian.horse_attach_document(id, request.form['doc-type'], request.form['doc-url'], request.form['doc-name'])
    else:
        equestrian.horse_add_document(id, request.form['doc-type'], request.files['file'])
    
    flash(f"Documento agregado exitosamente", "success")
    return redirect(url_for('ecuestre.show', id=id, initial_page=1))


@bp.post("/<int:id>/delete_document/<int:document_id>")
def delete_document(id: int, document_id: int)->str:
    """Recibe el ID de un caballo y el ID de un documento y lo elimina de la BD"""
    if not check_permission(session,"ecuestre_update"):
        return unauthorized()
    
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
