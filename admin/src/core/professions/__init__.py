from src.core.database import db
from src.core.professions.profession import Profession
from src.core.professions.job import Job


"""Módulo de profesiones"""
def get_professions():
    """Obtiene todas las profesiones"""
    return Profession.query.all()

def get_profession_by_id(profession_id):
    """Obtiene una profesion por ID"""
    return Profession.query.filter_by(id=profession_id).first()

def profession_new(**kwargs):
    """Crea una profesion, la guarda en la BD y la devuelve"""
    profession = Profession(**kwargs)
    db.session.add(profession)
    db.session.commit()
    return profession


"""Módulo de trabajos"""
def jobs():
    """Obtiene todos los trabajos"""
    return Job.query.all()

def get_job_by_id(job_id):
    """Obtiene un trabajo por ID"""
    return Job.query.filter_by(id=job_id).first()

def job_new(**kwargs):
    """Crea un trabajo, lo guarda en la BD y lo devuelve"""
    job = Job(**kwargs)
    db.session.add(job)
    db.session.commit()
    return job
