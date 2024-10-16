from flask import current_app
from src.core.database import db
from src.core.equestrian.horse import Horse
from src.core.equestrian.activity import Activity
from src.core.people.member_rider import Member
from src.core.equestrian.horse_document import HorseDocument
from src.core.equestrian.horse_document_types import HorseDocumentType
from werkzeug.utils import secure_filename
from ulid import ULID
from os import fstat
import os

UPLOAD_FOLDER = '/ecuestre_docs'
ALLOWED_DOC_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

def list_horses(order_by: str = 'name', order: str = 'asc', limit: int = 10, page: int = 1, search: str = '', activity_id: int = None):
    """Devuelve todos los caballos de la BD con paginación, orden y búsqueda"""
    query = Horse.query

    # Filtro de búsqueda por nombre
    if search:
        query = query.filter(Horse.name.ilike(f'%{search}%'))

    # Filtro de búsqueda por ID de actividad
    if activity_id:
        query = query.join(Horse.activities).filter(Activity.id == activity_id)

    # Ordenamiento
    order_column = getattr(Horse, order_by)
    if order == 'desc':
        order_column = order_column.desc()
    query = query.order_by(order_column)

    # Paginación
    paginated_query = query.paginate(page=page, per_page=limit, error_out=False)
    return paginated_query.items, paginated_query.pages

def get_drivers():
    """Obtiene todos los conductores"""
    return Member.query.filter_by(job_id=4).all()

def get_trainers():
    """Obtiene todos los entrenadores de caballos"""
    return Member.query.filter_by(job_id=8).all()

def get_horse_by_id(horse_id:int)->Horse:
    """Devuelve un caballo por ID"""
    return Horse.query.filter_by(id=horse_id).first()

def get_document_types()->list:
    """Devuelve todos los tipos de documentos"""
    return HorseDocumentType.query.all()

def get_horse_documents(horse_id: int, document_type_id: int = None, search: str = '', order_by: str = 'id', order: str = 'asc')->list:
    """Devuelve los documentos de un caballo por ID con URLs descargables"""
    docs_db = HorseDocument.query.filter_by(horse_id=horse_id)
    if document_type_id:
        docs_db = docs_db.filter_by(document_type_id=document_type_id)
    
    # Filtro de búsqueda por nombre
    if search:
        docs_db = docs_db.filter(HorseDocument.name.ilike(f'%{search}%'))
        
    # Ordenamiento
    order_column = getattr(HorseDocument, order_by)
    if order == 'desc':
        order_column = order_column.desc()
    docs_db = docs_db.order_by(order_column)
        
    docs = []
    for doc in docs_db:
        doc_url = current_app.storage._client.presigned_get_object("grupo04", doc.file_path) if doc.file_path else doc.url
        docs.append({
            'id': doc.id,
            'name': doc.name,
            'type': doc.document_type.name,
            'upload_date': doc.upload_date,
            'url': doc_url,
            'isFile': doc.file_path is not None
        })
    return docs


def horse_new(**kwargs)->Horse:
    """Crea un caballo, lo guarda en la BD y lo devuelve"""
    horse = Horse(**kwargs)
    db.session.add(horse)
    db.session.commit()
    return horse

def horse_update(horse_id: int, **kwargs) -> Horse:
    """Actualiza un caballo por ID y lo devuelve"""
    horse = get_horse_by_id(horse_id)
    
    # Actualizar atributos del caballo
    for attr, value in kwargs.items():
        if attr not in ['activities', 'members']:
            setattr(horse, attr, value)
    
    # Limpiar listas de actividades y miembros asignados
    horse.activities.clear()
    horse.assigned_members.clear()
    
    # Verificar y agregar actividades
    if 'activities' in kwargs:
        for activity_id in kwargs['activities']:
            activity = Activity.query.filter_by(id=activity_id).first()
            if activity:
                horse.activities.append(activity)
    
    # Verificar y agregar miembros
    if 'members' in kwargs:
        for member_id in kwargs['members']:
            member = Member.query.filter_by(id=member_id).first()
            if member:
                horse.assigned_members.append(member)
    
    # Confirmar cambios en la base de datos
    db.session.commit()
    return horse

def horse_delete(horse_id:int)->Horse:
    """Elimina un caballo por ID"""
    horse = get_horse_by_id(horse_id)
    
    # Eliminar documentos asociados
    for doc in horse.documents:
        delete_document(doc.id)
    
    db.session.delete(horse)
    db.session.commit()
    return horse

def horse_document_type_new(name:str)->HorseDocumentType:
    """Crea un nuevo tipo de documento y lo guarda en la BD"""
    document_type = HorseDocumentType(name=name)
    db.session.add(document_type)
    db.session.commit()
    return document_type

def horse_add_document(horse_id:int, document_type:int, file:bytes)->HorseDocument:
    """Añade un documento a un caballo por ID y lo guarda en MinIO"""
    
    # Verificar si el archivo es válido
    if not _allowed_file(file.filename):
        raise TypeError("El archivo no es válido")

    # Crear ULID
    ulid = ULID()
    
    # Sanitizar nombre de archivo
    filename = secure_filename(file.filename)
    
    # Generar path de archivo
    file_path = os.path.join(UPLOAD_FOLDER, f'${ulid}-{filename}')
    return _add_document(horse_id, document_type, file, file_path)

def horse_attach_document(horse_id:int, document_type:int, url:str, name: str = None)->HorseDocument:
    """Añade un documento a un caballo por ID y lo guarda en la BD"""
    return _attach_document(horse_id, document_type, url, name)


def _allowed_file(filename):
    """Verifica si la extensión del archivo es válida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_DOC_EXTENSIONS

def _attach_document(horse_id: int, document_type_id: int, url: str, name: str = None)->HorseDocument:
    """Añade una URL como documento a un caballo y lo guarda en la BD"""
    document = HorseDocument(
        name=name if name else url,
        horse_id=horse_id,
        document_type_id=document_type_id,
        url=url
    )
    db.session.add(document)
    db.session.commit()
    return document

def _add_document(horse_id: int, document_type_id: int, file: bytes, path: str)->HorseDocument:
    """Añade un documento a un caballo por ID y lo guarda en MinIO"""
    size = fstat(file.fileno()).st_size
    try:
        document = current_app.storage._client.put_object(
            "grupo04",
            path,
            file,
            size,
            file.content_type
        )
    except Exception as e:
        raise RuntimeError(f"Error subiendo el documento: {e}")

    document = HorseDocument(
        name = file.filename,
        horse_id=horse_id,
        document_type_id=document_type_id,
        file_path=path
    )
    
    db.session.add(document)
    db.session.commit()
    return document

def delete_document(document_id: int):
    """Elimina un documento por ID"""
    document = HorseDocument.query.filter_by(id=document_id).first()
    
    if document.file_path:
        current_app.storage.client.remove_object("grupo04", document.file_path)
        
    db.session.delete(document)
    db.session.commit()
    return document


"""Módulo de actividades"""
def list_activities()->list:
    """Obtiene todas las actividades"""
    return Activity.query.all()

def get_activity_by_id(activity_id:int)->Activity:
    """Obtiene una actividad por ID"""
    return Activity.query.filter_by(id=activity_id).first()

def activity_new(**kwargs)->Activity:
    """Crea una actividad, la guarda en la BD y la devuelve"""
    activity = Activity(**kwargs)
    db.session.add(activity)
    db.session.commit()
    return activity