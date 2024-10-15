from src.core.professions.profession import Profession
from src.core.professions.job import Job
from src.core.professions.job_proposal import JobProposal
from src.core.professions.school import School
from src.web.forms.rider_form import RiderForm
from src.core import database_functions as db


"""Módulo de profesiones"""

def list_professions() -> list:
    """Obtiene todas las profesiones"""
    return db.list_all(Profession)


def get_profession_by_id(profession_id: int) -> Profession:
    """Obtiene una profesion por ID"""
    return db.get_by_field(Profession, "id", profession_id)


def profession_new(**kwargs) -> Profession:
    """Crea una profesion, la guarda en la BD y la devuelve"""
    return db.new(Profession, **kwargs)


"""Módulo de trabajos"""

def list_jobs() -> list:
    """Obtiene todos los trabajos"""
    return db.list_all(Job)

def get_job_by_id(job_id: int) -> Job:
    """Obtiene un trabajo por ID"""
    return db.get_by_field(Job, "id", job_id)


def job_new(**kwargs) -> Job:
    """Crea un trabajo, lo guarda en la BD y lo devuelve"""
    return db.new(Job, **kwargs)


"""Módulo de jya"""

def school_new(form:RiderForm, rider_id:int) -> int:
    """Recibe el formulario y el id del j/a y retorna la escuela creada"""
    school = School()
    if form.has_school.data == "True":
        school = db.new(**form.get_school_data(), rider_id=rider_id)
    return school


def job_proposal_new(form:RiderForm, rider_id:int) -> int:
    """Recibe el formulario y el id del j/a y retorna la propuesta de trabajo creada"""
    job_proposal = JobProposal()
    if form.has_job_proposal.data == "True":
        job_proposal = db.new(**form.get_job_proposal_data(), rider_id=rider_id)
    return job_proposal


def job_proposal_delete(id:int) -> JobProposal:
    """Recibe el id de una propuesta de trabajo, la elimina de la BD y la devuelve"""
    return db.delete(JobProposal, id)


def school_delete(id:int) -> School:
    """Recibe el id de una escuela, la elimina de la BD y la devuelve"""
    return db.delete(School, id)
