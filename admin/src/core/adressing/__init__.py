from src.core.adressing.province import Province
from src.core.adressing.locality import Locality
from src.core import database_functions as db

"""Módulo de provincias"""

def list_provinces() -> list:
    """Obtiene todas las provincias"""
    return db.list_all(Province)


def get_province_by_id(province_id: int) -> Province:
    """Obtiene una provincia por ID"""
    return db.get_by_field(Province, "id", province_id)


def province_new(**kwargs) -> Province:
    """Crea una provincia, la guarda en la BD y la devuelve"""
    return db.new(Province, **kwargs)


"""Módulo de localidades"""

def list_localities() -> list:
    """Obtiene todas las localidades con solo id y name"""
    return db.list_all(Locality)


def get_locality_by_id(locality_id: int) -> Locality:
    """Obtiene una localidad por ID"""
    return db.get_by_field(Locality, "id", locality_id)


def get_localities_by_province(province_id: int) -> list:
    """Obtiene todas las localidades de una provincia"""
    return db.filter(Locality, {"province_id": province_id})


def locality_new(**kwargs) -> Locality:
    """Crea una localidad, la guarda en la BD y la devuelve"""
    return db.new(Locality, **kwargs)
