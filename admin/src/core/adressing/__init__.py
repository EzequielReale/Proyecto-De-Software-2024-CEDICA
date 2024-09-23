from src.core.database import db
from src.core.adressing.province import Province
from src.core.adressing.locality import Locality


def get_province_by_id(province_id):
    return db.session.query(Province).filter(Province.id == province_id).first()

def get_locality_by_id(locality_id):
    return db.session.query(Locality).filter(Locality.id == locality_id).first()

def get_localities_by_province(province_id):
    return db.session.query(Locality).filter(Locality.province_id == province_id).all()

def get_provinces():
    return db.session.query(Province).all()

def get_localities():
    return db.session.query(Locality).all()

def province_new(**kwargs):
    """Crea una provincia, la guarda en la BD y la devuelve"""
    province = Province(**kwargs)
    db.session.add(province)
    db.session.commit()
    return province

def locality_new(**kwargs):
    """Crea una localidad, la guarda en la BD y la devuelve"""
    locality = Locality(**kwargs)
    db.session.add(locality)
    db.session.commit()
    return locality