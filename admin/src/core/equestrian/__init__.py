from src.core.database import db
from src.core.equestrian.horse import Horse
from src.core.equestrian.activity import Activity


def list_horses(order_by: str = 'name', order: str = 'asc', limit: int = 10, page: int = 1):
    """Devuelve todos los caballos de la BD con paginación y orden"""
    order_column = getattr(Horse, order_by)
    if order == 'desc':
        order_column = order_column.desc()
    query = Horse.query.order_by(order_column).paginate(page=page, per_page=limit, error_out=False)
    return query.items, query.pages

def get_horse_by_id(horse_id:int)->Horse:
    """Devuelve un caballo por ID"""
    return Horse.query.filter_by(id=horse_id).first()

def horse_new(**kwargs)->Horse:
    """Crea un caballo, lo guarda en la BD y lo devuelve"""
    horse = Horse(**kwargs)
    db.session.add(horse)
    db.session.commit()
    return horse

def horse_update(horse_id:int, **kwargs)->Horse:
    """Actualiza un caballo por ID y lo devuelve"""
    horse = get_horse_by_id(horse_id)
    for attr, value in kwargs.items():
        setattr(horse, attr, value)
    db.session.commit()
    return horse

def horse_delete(horse_id:int)->Horse:
    """Elimina un caballo por ID"""
    horse = get_horse_by_id(horse_id)
    db.session.delete(horse)
    db.session.commit()
    return horse


"""Módulo de actividades"""
def list_activities()->list:
    """Obtiene todas las actividades"""
    return Activity.query.all()

def get_activity_by_id(activity_id:int)->Activity:
    """Obtiene un trabajo por ID"""
    return Activity.query.filter_by(id=activity_id).first()

def activity_new(**kwargs)->Activity:
    """Crea una actividad, la guarda en la BD y la devuelve"""
    activity = Activity(**kwargs)
    db.session.add(activity)
    db.session.commit()
    return activity