from src.core.database import db
from src.core.adressing.province import Province
from src.core.adressing.locality import Locality

"""Módulo de provincias"""
def list_provinces()->list:
    """Obtiene todas las provincias"""
    return db.session.query(Province).all()

def get_province_by_id(province_id:int)->Province:
    """Obtiene una provincia por ID"""
    return db.session.query(Province).filter(Province.id == province_id).first()

def province_new(**kwargs)->Province:
    """Crea una provincia, la guarda en la BD y la devuelve"""
    province = Province(**kwargs)
    db.session.add(province)
    db.session.commit()
    return province

"""Módulo de localidades"""
def list_localities()->list:
    """Obtiene todas las localidades"""
    return db.session.query(Locality).all()

def get_locality_by_id(locality_id:int)->Locality:
    """Obtiene una localidad por ID"""
    return db.session.query(Locality).filter(Locality.id == locality_id).first()

def get_localities_by_province(province_id:int)->list:
    """Obtiene todas las localidades de una provincia"""
    return db.session.query(Locality).filter(Locality.province_id == province_id).all()

def locality_new(**kwargs)->Locality:
    """Crea una localidad, la guarda en la BD y la devuelve"""
    locality = Locality(**kwargs)
    db.session.add(locality)
    db.session.commit()
    return locality
