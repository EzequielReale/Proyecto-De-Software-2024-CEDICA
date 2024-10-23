from src.core import database_functions as db
from src.core.disabilities.disability_diagnosis import DisabilityDiagnosis
from src.core.disabilities.disability_type import DisabilityType


def list_disability_types() -> list:
    """Obtiene todos los tipos de discapacidad"""
    return db.list_all(DisabilityType)


def list_disability_diagnosis() -> list:
    """Obtiene todos los diagnósticos de discapacidad"""
    return db.list_all(DisabilityDiagnosis)


def get_disability_type_by_id(type_id: int) -> DisabilityType:
    """Obtiene un tipo de discapacidad por ID"""
    return db.get_by_field(DisabilityType, "id", type_id)


def get_diagnosis_by_type(type_id: int) -> list:
    """Obtiene todos los diagnósticos de discapacidad de un tipo"""
    return db.filter(DisabilityDiagnosis, {"type_id": type_id})


def disability_type_new(name:str) -> DisabilityType:
    """Crea un tipo de discapacidad, lo guarda en la BD y lo devuelve"""
    return db.new(DisabilityType, name=name)


def disability_diagnosis_new(name:str, type:DisabilityType) -> DisabilityDiagnosis:
    """Crea un diagnóstico de discapacidad, lo guarda en la BD y lo devuelve"""
    return db.new(DisabilityDiagnosis, name=name, type=type)
