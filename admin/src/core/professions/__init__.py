from src.core.database import db
from src.core.professions.profession import Profession
from src.core.professions.job import Job
from src.core.professions.job_proposal import JobProposal
from src.core.professions.school import School


"""Módulo de profesiones"""

def list_professions() -> list:
    """Obtiene todas las profesiones"""
    return Profession.query.all()


def get_profession_by_id(profession_id: int) -> Profession:
    """Obtiene una profesion por ID"""
    return Profession.query.filter_by(id=profession_id).first()


def profession_new(**kwargs) -> Profession:
    """Crea una profesion, la guarda en la BD y la devuelve"""
    profession = Profession(**kwargs)
    db.session.add(profession)
    db.session.commit()
    return profession


"""Módulo de trabajos"""

def list_jobs() -> list:
    """Obtiene todos los trabajos"""
    return Job.query.all()


def get_job_by_id(job_id: int) -> Job:
    """Obtiene un trabajo por ID"""
    return Job.query.filter_by(id=job_id).first()


def job_new(**kwargs) -> Job:
    """Crea un trabajo, lo guarda en la BD y lo devuelve"""
    job = Job(**kwargs)
    db.session.add(job)
    db.session.commit()
    return job


"""Módulo de jya"""

def job_proposal_new(**kwargs) -> JobProposal:
    """Crea una propuesta de trabajo, la guarda en la BD y la devuelve"""
    job_proposal = JobProposal(**kwargs)
    db.session.add(job_proposal)
    db.session.commit()
    return job_proposal


def school_new(**kwargs) -> School:
    """Crea una escuela, la guarda en la BD y la devuelve"""
    school = School(**kwargs)
    db.session.add(school)
    db.session.commit()
    return school
