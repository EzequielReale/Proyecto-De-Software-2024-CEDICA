from io import BytesIO
from os import fstat
import uuid

from flask import current_app, send_file
from minio.error import S3Error

from src.core import adressing, database_functions as db_fun, professions
from src.core.database import db
from src.core.people.member_rider import Member, Rider, UserMember
from src.core.people.person_document import PersonDocument as Document
from src.core.people.tutor import Tutor
from src.web.forms.rider_form import RiderForm


"""Funciones de documentos"""

def document_new(person_id: int, path: str, name: str, type:str=None, link:bool=False) -> Document:
    """Crea un documento, lo guarda en la BD y lo devuelve"""
    document = Document(
        person_id=person_id,
        document_path=path,
        document_name=name,
        document_type=type,
        its_a_link=link
    )
    db.session.add(document)
    db.session.commit()
    return document


def _save_document(file: bytes, path: str) -> bytes:
    """Guarda un documento en MinIO y lo devuelve"""
    size = fstat(file.fileno()).st_size
    try:
        document = current_app.storage.client.put_object(
            "grupo04", path, file, size, file.content_type
        )
        return document
    except S3Error as e:
        raise RuntimeError(f"Error subiendo el documento: {e}")


def _get_files_associated(docs:tuple) -> list:
    """Devuelve los documentos reales asociados a los documentos de la BD"""
    files = []
    for doc in docs:
        if doc.its_a_link:
            file_url = doc.document_path
        else:
            file_url = current_app.storage.client.presigned_get_object(
                "grupo04", doc.document_path
            )
        files.append(
            {
                "id": doc.id,
                "name": doc.document_name,
                "url": file_url,
                "type": doc.document_type,
                "its_a_link": doc.its_a_link,
                "created_at": doc.created_at,
            }
        )
    return files


def list_documents(person_id: int) -> list:
    """Devuelve los documentos de una persona por ID con URLs descargables"""
    docs_db = db_fun.filter(Document, {"person_id": person_id})
    return _get_files_associated(docs_db)


def list_filtered_documents(person_id: int, filters: dict, sort_by=None, sort_direction="asc") -> list:
    """Devuelve los documentos de una persona por ID y filtros aplicados con URLs descargables"""
    docs_db = db_fun.filter(Document, filters)
    docs_db = db_fun.order_by(Document, docs_db, sort_by, sort_direction)
    return _get_files_associated(docs_db)


def get_document_by_id(document_id: int) -> Document:
    """Devuelve un documento por ID"""
    return db_fun.get_by_field(Document, "id", document_id)


def update_document(document:Document, **kwargs) -> Document:
    """Recibe un documento, lo edita y lo devuelve"""    
    if not document.its_a_link:
        current_app.storage.client.remove_object("grupo04", document.document_path)
        _save_document(kwargs["file"], document.document_path)
    else:
        db_fun.update(Document, document.id, **kwargs)
        
    return document


def delete_document(document_id: int) -> Document:
    """Elimina un documento por ID y lo devuelve"""
    document = db_fun.get_by_field(Document, "id", document_id)
    if not document.its_a_link:
        current_app.storage.client.remove_object("grupo04", document.document_path)
    db.session.delete(document)
    db.session.commit()
    return document


def download_document(document_id: int) -> bytes:
    """Descarga un documento por ID, obteniendo su contenido desde MinIO"""
    document = db_fun.get_by_field(Document, "id", document_id)

    try:
        # Obtener el archivo desde MinIO
        file_obj = current_app.storage.client.get_object("grupo04", document.document_path)
        
        # Leer el contenido del archivo
        file_data = BytesIO(file_obj.read())

        # Devolver el archivo como descarga
        return send_file(
            file_data,
            as_attachment=True,
            download_name=document.document_name,
            mimetype="application/octet-stream"
        )
    except S3Error as e:
        raise RuntimeError(f"Error descargando el documento: {e}")


"""Funciones de miembros"""

def list_members(filters: dict, page=1, per_page=25, sort_by=None, sort_direction="asc") -> tuple:
    """Devuelve miembros que coinciden con los filtros enviados como parámetro"""
    return db_fun.list_paginated(Member, filters, page, per_page, sort_by, sort_direction)


def get_member_by_field(field: str, value, exclude_id=None) -> Member:
    """Devuelve un miembro por un campo específico y su valor"""
    return db_fun.get_by_field(Member, field, value, exclude_id)


def member_new(**kwargs) -> Member:
    """Crea un miembro, lo guarda en la BD y lo devuelve"""
    return db_fun.new(Member, **kwargs)


def member_update(member_id: int, **kwargs) -> Member:
    """Actualiza un miembro por ID y lo devuelve"""
    return db_fun.update(Member, member_id, **kwargs)


def member_delete(member_id: int) -> Member:
    """Elimina un miembro por ID y lo devuelve"""
    # Eliminar documentos asociados
    documents = list_documents(member_id)
    for document in documents:
        delete_document(document["id"])

    # Quitar el miembro de los j/a asociados
    riders = db_fun.filter(Rider, {'members': member_id})
    for rider in riders:
        rider.members = [m for m in rider.members if m.id != member_id]
        db.session.commit()

    # Quitar el miembro de las propuestas de trabajo de J/a asociadas
    job_proposals = set()
    job_proposals.update(db_fun.filter(professions.JobProposal, {"professor_id": member_id}))
    job_proposals.update(db_fun.filter(professions.JobProposal, {"member_horse_rider_id": member_id}))
    job_proposals.update(db_fun.filter(professions.JobProposal, {"assistant_id": member_id}))
    for job_proposal in job_proposals:
        professions.job_proposal_delete(job_proposal.id)

    # Borrar la relación con el usuario asociado (si tiene)
    user_member = db_fun.get_by_field(UserMember, "member_id", member_id)
    if user_member:
        db_fun.delete_by_field(UserMember, "member_id", member_id)

    return db_fun.delete(Member, member_id)


def member_add_document(member_id: int, file: bytes) -> Document:
    """Añade un documento a un miembro por ID y lo guarda en MinIO"""
    ulid = uuid.uuid4().hex
    path = f"members/{member_id}/{ulid}_{file.filename}"
    _save_document(file, path)
    return document_new(member_id, path, file.filename)


"""Funciones de j/a"""

def list_riders(filters: dict, page=1, per_page=25, sort_by=None, sort_direction="asc") -> tuple:
    """Devuelve los jinetes paginados de la BD"""
    return db_fun.list_paginated(Rider, filters, page, per_page, sort_by, sort_direction)


def get_rider_by_field(field: str, value, exclude_id=None) -> Rider:
    """Devuelve un jinete por un campo específico y su valor"""
    return db_fun.get_by_field(Rider, field, value, exclude_id)


def _create_rider(form:RiderForm) -> int:
    """Recibe el formulario y retorna el id del j/a creado"""
    tutor_1, tutor_2 = _create_tutors(form)
    rider_data = form.get_rider_data()
    rider_data['locality'] = adressing.get_locality_by_id(rider_data['locality_id'])
    rider_data['city_of_birth'] = adressing.get_locality_by_id(rider_data['city_of_birth'])
    rider_data['tutor_1'] = tutor_1 if tutor_1 else None
    rider_data['tutor_2'] = tutor_2 if tutor_2 else None
    member_ids = form.assigned_professionals.data
    rider_data['members'] = [get_member_by_field("id", member_id) for member_id in member_ids]

    return db_fun.new(Rider, **rider_data)


def _create_tutors(form:RiderForm) -> Tutor:
    """Recibe el formulario y retorna los tutores creados"""
    tutor_1 = None
    tutor_2 = None

    if form.has_tutor_1.data == "True":
        tutor_1 = db_fun.new(Tutor, **form.get_tutor_data(1))
    if form.has_tutor_2.data == "True":
        tutor_2 = db_fun.new(Tutor, **form.get_tutor_data(2))
    
    return tutor_1, tutor_2


def rider_new(form:RiderForm) -> str:
    """Crea un nuevo jinete en base a un formulario, lo guarda en la BD y lo devuelve"""
    rider = _create_rider(form)
    professions.school_new(form, rider.id)
    professions.job_proposal_new(form, rider.id)
    return rider



def rider_update(rider_id: int,  form: PartialRiderForm) -> Rider:
    """Actualiza un jinete por ID y lo devuelve"""
    rider = get_rider_by_field("id", rider_id)
    rider_data = form.get_rider_data() 
    print(rider_data)

    rider_data['locality'] = adressing.get_locality_by_id(rider_data['locality_id'])
    rider_data['city_of_birth'] = adressing.get_locality_by_id(rider_data['city_of_birth'])

    for attr, value in rider_data.items():
        setattr(rider, attr, value)  

    db.session.commit()  
    return rider 


def update_rider_tutor(rider_id: int, form: TutorRiderForm) -> Rider:
    """Actualiza la información de los tutores de un jinete/amazona por ID y lo devuelve"""
    rider = get_rider_by_field("id", rider_id)
    tutor1_data = form.get_tutor_data(1)  
    tutor2_data = form.get_tutor_data(2)

    if form.has_tutor_1.data == "True": #No va a pasar que esto sea false por las validaciones
         if rider.tutor_1 is not None:
           for attr, value in tutor1_data.items():
             setattr(rider.tutor_1, attr, value)
         else:
             rider.tutor_1 = tutor_new_seed(**tutor1_data)  #lo creo y asigno
    

    if form.has_tutor_2.data == "True":
         if rider.tutor_2 is not None:
           for attr, value in tutor2_data.items():
             setattr(rider.tutor_2, attr, value)
         else:
             rider.tutor_2= tutor_new_seed(**tutor2_data)
    else:
        rider.tutor_2=None

    db.session.commit()
    return rider





def rider_delete(rider_id: int) -> Rider:
    """Elimina un jinete por ID y lo devuelve"""
    rider = db_fun.get_by_field(Rider, "id", rider_id)

    documents = list_documents(rider.id)
    for document in documents:
        delete_document(document["id"])

    if rider.tutor_1:
        db_fun.delete(Tutor, rider.tutor_1.id)
    if rider.tutor_2:
        db_fun.delete(Tutor, rider.tutor_2.id)
    if rider.school:
        professions.school_delete(rider.school.id)
    if rider.job_proposal:
        professions.job_proposal_delete(rider.job_proposal.id)

    return db_fun.delete(Rider, rider_id)


def rider_add_document(rider_id: int, file: bytes, type:str) -> Document:
    """Añade un documento a un jinete por ID y lo guarda en MinIO"""
    ulid = uuid.uuid4().hex
    path = f"riders/{rider_id}/{ulid}_{file.filename}"
    _save_document(file, path)
    return document_new(rider_id, path, file.filename, type)

"""Seeds"""

def rider_new_seed(**kwargs) -> Rider:
    """Crea un jinete con datos de prueba y lo guarda en la BD"""
    return db_fun.new(Rider, **kwargs)

def school_new_seed(**kwargs) -> professions.School:
    """Crea una escuela con datos de prueba y la guarda en la BD"""
    return db_fun.new(professions.School, **kwargs)

def job_proposal_new_seed(**kwargs) -> professions.JobProposal:
    """Crea una propuesta de trabajo con datos de prueba y la guarda en la BD"""
    return db_fun.new(professions.JobProposal, **kwargs)

def tutor_new_seed(**kwargs) -> Tutor:
    """Crea un tutor con datos de prueba y lo guarda en la BD"""
    return db_fun.new(Tutor, **kwargs)
