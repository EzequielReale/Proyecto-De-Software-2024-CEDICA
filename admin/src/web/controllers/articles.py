from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from src.core import content_admin as content
from src.core.content_admin.article_status_enum import ArticleStatus
from src.web.handlers.autenticacion import check_permission, login_required
from src.web.handlers.error import unauthorized

bp=Blueprint("articles",__name__, url_prefix="/articles")

@bp.get("/")
@login_required
def index():
    if not check_permission(session, "content_index"):
        return unauthorized()

    limit = int(request.args.get('limit', 6))
    page = int(request.args.get('page', 1))
    
    articles, total_pages = content.list_articles(limit=limit, page=page)
    
    return render_template("articles/index.html", articles=articles, article_status=ArticleStatus, limit=limit, page=page, total_pages=total_pages)

@bp.get("/<int:id>")
@login_required
def show(id: int):
    """Detalle de un caballo en específico"""
    if not check_permission(session,"content_show"):
        return unauthorized()
        
    res = content.get_article_by_id(id)
    return render_template('articles/show.html', article=res, article_status=ArticleStatus)

@bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if not check_permission(session,"content_new"):
        return unauthorized()
     
    # Si no se envía el formulario
    if request.method == 'GET':
        return render_template('articles/create.html')
    
    # Si se envía el formulario, se procede con la creación del caballo
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

    # Validar los datos del formulario
    errors = validate_horse_form(form_data)

    # Si hay errores, mostrar mensajes de error y renderizar el formulario nuevamente
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('ecuestre/create.html', form_data=form_data, activities=equestrian.list_activities(), drivers=equestrian.get_drivers(), trainers=equestrian.get_trainers())
    
    horse = equestrian.horse_new_from_form(form_data)
    flash(f"Caballo creado exitosamente", "success")
    return redirect(url_for('ecuestre.show', id=horse.id))


@bp.route("/<int:id>/update", methods=['GET', 'POST'])
def update(id: int)->str:
    """Recibe el id de un caballo y muestra el formulario para editarlo, o lo actualiza en caso de que se envíe el formulario"""
    if not check_permission(session,"content_update"):
        return unauthorized()
     
    horse = equestrian.get_horse_by_id(id)
    
    if not horse:
        flash(f"El caballo con ID {id} no existe", "danger")
        return redirect(url_for('ecuestre.index'))

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

        # Validar los datos del formulario
        errors = validate_horse_form(form_data)

        # Si hay errores, mostrar mensajes de error y renderizar el formulario nuevamente
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('ecuestre/update.html', horse=horse_dict, activities=equestrian.list_activities(), drivers=equestrian.get_drivers(), trainers=equestrian.get_trainers())

        # Convertir los datos del formulario a los valores correctos
        form_data['gender']="Macho" if form_data['gender'] == 0 else "Hembra"
        form_data['donation']=form_data['origin'] == 1

        # Edición del caballo
        equestrian.horse_update(
            horse_id=horse.id,
            form_data=form_data
        )
        
        flash(f"Caballo actualizado exitosamente", "success")
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
        
    return render_template('ecuestre/update.html', horse=horse_dict, activities=equestrian.list_activities(), drivers=equestrian.get_drivers(), trainers=equestrian.get_trainers())


@bp.post("/<int:id>/delete")
@login_required
def destroy(id: int):
    """Eliminar un caballo de la institución"""
    if not check_permission(session,"content_destroy"):
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
    if not check_permission(session,"content_update"):
        return unauthorized()
    
    if not equestrian.get_horse_by_id(id):
        flash(f"El caballo con ID {id} no existe", "danger")
        return redirect(url_for('ecuestre.index'))
    
    if 'file' not in request.files:
        equestrian.horse_attach_document(id, request.form['doc-type'], request.form['doc-url'], request.form['doc-name'])
    else:
        # Si se envía un archivo, valido que esté dentro de las extensiones permitidas
        if not equestrian.allowed_file(request.files['file'].filename):
            flash(f"El archivo {request.files['file'].filename} no es un formato permitido", "danger")
            return redirect(url_for('ecuestre.show', id=id, initial_page=1))
        
        equestrian.horse_add_document(id, request.form['doc-type'], request.files['file'])
    
    flash(f"Documento agregado exitosamente", "success")
    return redirect(url_for('ecuestre.show', id=id, initial_page=1))


@bp.post("/<int:id>/delete_document/<int:document_id>")
def delete_document(id: int, document_id: int)->str:
    """Recibe el ID de un caballo y el ID de un documento y lo elimina de la BD"""
    if not check_permission(session,"content_update"):
        return unauthorized()
    
    if not equestrian.get_horse_by_id(id):
        flash(f"El caballo con ID {id} no existe", "danger")
        return redirect(url_for('ecuestre.index'))
    
    if not equestrian.get_document_by_id(document_id):
        flash(f"El documento con ID {document_id} no existe", "danger")
        return redirect(url_for('ecuestre.show', id=id, initial_page=1))
    
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
