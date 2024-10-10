from src.core.database import db
from src.core.disabilities.disability_diagnosis import DisabilityDiagnosis
from src.core.disabilities.disability_type import DisabilityType


def list_disability_types() -> list:
    """Obtiene todos los tipos de discapacidad"""
    return db.session.query(DisabilityType).all()


def list_disability_diagnosis() -> list:
    """Obtiene todos los diagnósticos de discapacidad"""
    return db.session.query(DisabilityDiagnosis).all()


def get_disability_type_by_id(type_id: int) -> DisabilityType:
    """Obtiene un tipo de discapacidad por ID"""
    return db.session.query(DisabilityType).filter(DisabilityType.id == type_id).first()


def get_diagnosis_by_type(type_id: int) -> list:
    """Obtiene todos los diagnósticos de discapacidad de un tipo"""
    return (
        db.session.query(DisabilityDiagnosis)
        .filter(DisabilityDiagnosis.type_id == type_id)
        .all()
    )


def disability_type_new(**kwargs) -> DisabilityType:
    """Crea un tipo de discapacidad, lo guarda en la BD y lo devuelve"""
    disability_type = DisabilityType(**kwargs)
    db.session.add(disability_type)
    db.session.commit()
    return disability_type


def disability_diagnosis_new(**kwargs) -> DisabilityDiagnosis:
    """Crea un diagnóstico de discapacidad, lo guarda en la BD y lo devuelve"""
    diagnosis = DisabilityDiagnosis(**kwargs)
    db.session.add(diagnosis)
    db.session.commit()
    return diagnosis
