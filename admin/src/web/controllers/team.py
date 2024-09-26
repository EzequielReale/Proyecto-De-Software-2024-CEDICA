from flask import render_template, Blueprint, request, redirect, url_for

from src.core import people


bp = Blueprint("team", __name__, url_prefix ="/team") 

@bp.get("/")
def index():
    """Listado de miembros del equipo"""
    members = people.list_members()
    return render_template('team/index.html', members=members)

@bp.get("/<int:id>")
def show(id: int):
    """Detalle de un miembro del equipo"""
    member = people.get_member_by_id(id)
    return render_template('team/show.html', member=member)

@bp.get("/nuevo")
def create():
    """Formulario para crear un nuevo miembro del equipo"""
    return render_template('team/create.html')

@bp.get("/<int:id>/editar")
def update(id: int):
    """Formulario para editar un miembro del equipo"""
    member = people.get_member_by_id(id)
    return render_template('team/update.html', member=member)

@bp.post("/")
def store():
    """Guardar un nuevo miembro del equipo"""
    member = people.member_new(**request.form)
    return redirect(url_for('team.show', id=member.id))

@bp.post("/<int:id>")
def save(id: int):
    """Actualizar un miembro del equipo"""
    member = people.member_update(id, **request.form)
    return redirect(url_for('team.show', id=member.id))

@bp.post("/<int:id>/eliminar")
def destroy(id: int):
    """Eliminar un miembro del equipo"""
    member = people.member_delete(id)
    return redirect(url_for('team.index'))
