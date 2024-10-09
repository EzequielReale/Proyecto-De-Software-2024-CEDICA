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
from ulid import ULID
from os import fstat
import os

bp=Blueprint("ecuestre",__name__,url_prefix="/ecuestre")

UPLOAD_FOLDER = '/ecuestre'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

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
            
        # Obtener los miembros asignados
        assigned_members = request.form.get('assigned_members')
        if assigned_members:
            assigned_members = json.loads(assigned_members)
            
        # Crear el caballo
        horse = equestrian.horse_new(
            name=name,
            birth_date=birth_date,
            entry_date=entry_date,
            gender=gender,
            origin=origin,
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

def allowed_file(filename):
    """Verifica si la extensión del archivo es válida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_file():
    """Subir un archivo de ecuestre a Minio"""
    if 'file' not in request.files:
        # No se seleccionó archivo
        return jsonify(success=False, message='No file part')
    file = request.files['file']
    if file.filename == '':
        # No se seleccionó archivo
        return jsonify(success=False, message='No selected file')
    if file and allowed_file(file.filename):
        # Sanitizar nombre de archivo
        filename = secure_filename(file.filename)
        
        # Obtengo cliente de Minio
        client = current_app.storage._client
        
        # Obtengo el size del archivo para poder subirlo
        size = fstat(file.fileno()).st_size
        
        # Creo un ULID para el nombre del archivo
        ulid = ULID()
        
        # Subo el archivo a Minio
        client.put_object('grupo04', f'${ulid}-{filename}', file, size, content_type=file.content_type)
        
        # Devuelvo la URL del archivo
        file_path = os.path.join(UPLOAD_FOLDER, f'${ulid}-{filename}')
        return jsonify(success=True, filePath=file_path)
    
    # Devuelvo un error si el archivo no es válido
    return jsonify(success=False, message='File not allowed')
