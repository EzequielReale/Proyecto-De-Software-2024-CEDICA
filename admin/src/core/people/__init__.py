from io import BytesIO
from os import fstat
import uuid
from typing import List

from flask import current_app, send_file
from flask import request
from minio.error import S3Error

from src.core import adressing, database_functions as db_fun, professions, registro_pagos_jya
from src.core.database import db
from src.core.people.member_rider import Member, Rider, UserMember
from src.core.people.person_document import PersonDocument as Document
from src.core.people.tutor import Tutor
from src.web.forms.rider_form import RiderForm
from src.web.forms.rider_update_form import PartialRiderForm,TutorRiderForm, SchoolJobRiderForm


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


def tutor_new(**kwargs) -> Tutor:
    """Crea un tutor y lo guarda en la BD"""
    return db_fun.new(Tutor, **kwargs)


def _create_tutors(form:RiderForm) -> Tutor:
    """Recibe el formulario y retorna los tutores creados"""
    tutor_1 = None
    tutor_2 = None

    if form.has_tutor_1.data == "True":
        tutor_1 = tutor_new(**form.get_tutor_data(1))
    if form.has_tutor_2.data == "True":
        tutor_2 = tutor_new(**form.get_tutor_data(2))
    
    return tutor_1, tutor_2

def has_debt(rider_id: int) -> bool:
    """Devuelve True si el jinete tiene deudas, False en caso contrario"""
    rider = get_rider_by_field("id", rider_id)
    return db_fun.filter(registro_pagos_jya.PagoJineteAmazona, {"jinete_amazona_id": rider_id, "en_deuda": True}).count() > 0


def rider_new(form:RiderForm) -> str:
    """Crea un nuevo jinete en base a un formulario, lo guarda en la BD y lo devuelve"""
    rider = _create_rider(form)
    professions.school_new(form, rider.id)
    professions.job_proposal_new(form, rider.id)
    return rider

#updates----

def rider_update(rider_id: int,  form: PartialRiderForm) -> Rider:
    """Actualiza un jinete por ID y lo devuelve"""
    rider = get_rider_by_field("id", rider_id)
    rider_data = form.get_rider_data() 
    
    rider_data['locality'] = adressing.get_locality_by_id(rider_data['locality_id'])
    rider_data['city_of_birth'] = adressing.get_locality_by_id(rider_data['city_of_birth'])

    db_fun.update(Rider, rider_id, **rider_data) 
    return rider 


def update_rider_tutor(rider_id: int, form: TutorRiderForm) -> Rider:
    """Actualiza la información de los tutores de un jinete/amazona por ID y lo devuelve"""
    rider = get_rider_by_field("id", rider_id)
    tutor1_data = form.get_tutor_data(1)  
    tutor2_data = form.get_tutor_data(2)

    if form.has_tutor_1.data == "True":
        if rider.tutor_1 is not None:
           db_fun.update(Tutor, rider.tutor_1.id, **tutor1_data)  # si existe lo actualizo
        else:
            rider.tutor_1 = tutor_new(**tutor1_data)  # si no existe lo creo y asigno
    else:
        if rider.tutor_1 is not None:
            db_fun.delete(Tutor, rider.tutor_1.id) # si lo quiere eliminar (y existe) lo elimino

    if form.has_tutor_1.data == "True" and form.has_tutor_2.data == "True":
        print("entro")
        if rider.tutor_2 is not None:
            db_fun.update(Tutor, rider.tutor_2.id, **tutor2_data)
        else:
            rider.tutor_2 = tutor_new(**tutor2_data)
            db.session.commit()
    else:
        if rider.tutor_2 is not None:
            db_fun.delete(Tutor, rider.tutor_2.id)

    return rider


def update_school_job(rider_id: int, form: SchoolJobRiderForm) -> Rider:
    """Actualiza y/o crea la información de la escuela y/o trabajo del rider, y lo devuelve """
    rider = get_rider_by_field("id", rider_id)
    school_data = form.get_school_data()  
    job_data = form.get_job_proposal_data()


    if form.has_school.data =="True":
        if rider.school is not None:
            db_fun.update(professions.School, rider.school.id, **school_data) # si existe lo actualizo
        else:
            professions.school_new(form, rider_id=rider.id) # si no existe lo creo
    else: #lo quiere eliminar
        if rider.school is not None:
            professions.school_delete(rider.school.id) # si existe y lo quiere eliminar lo elimino

    if form.has_job_proposal.data == "True":
        if rider.job_proposal is not None:
            db_fun.update(professions.JobProposal, rider.job_proposal.id, **job_data)
        else:
            professions.job_proposal_new(form, rider_id=rider.id)
    else: 
        if rider.job_proposal is not None:
            professions.job_proposal_delete(rider.job_proposal.id)
    return rider


def update_professional_rider(rider_id: int, professional_ids: list) -> Rider:
    rider = get_rider_by_field("id", rider_id)
    assigned_professionals = db.session.query(Member).filter(Member.id.in_(professional_ids)).all()
    
    rider.members.clear()  # Elimina los profesionales asignados anteriormente
    rider.members.extend(assigned_professionals) # Asigna los nuevos profesionales 
    db.session.commit()
    return rider

#-----

def rider_delete(rider_id: int) -> Rider:
    """Elimina un jinete por ID y lo devuelve"""
    rider = db_fun.get_by_field(Rider, "id", rider_id)

    documents = list_documents(rider.id)
    for document in documents:
        delete_document(document["id"])

    return db_fun.delete(Rider, rider_id)


def rider_add_document(rider_id: int, file: bytes, type:str) -> Document:
    """Añade un documento a un jinete por ID y lo guarda en MinIO"""
    ulid = uuid.uuid4().hex
    path = f"riders/{rider_id}/{ulid}_{file.filename}"
    _save_document(file, path)
    return document_new(rider_id, path, file.filename, type)

"""Seeds"""

def school_new_seed(**kwargs) -> professions.School:
    """Crea una escuela con datos de prueba y la guarda en la BD"""
    return db_fun.new(professions.School, **kwargs)


def job_proposal_new_seed(**kwargs) -> professions.JobProposal:
    """Crea una propuesta de trabajo con datos de prueba y la guarda en la BD"""
    return db_fun.new(professions.JobProposal, **kwargs)


def rider_new_seed(**kwargs) -> Rider:
    """Crea un jinete con datos de prueba y lo guarda en la BD"""
    return db_fun.new(Rider, **kwargs)
