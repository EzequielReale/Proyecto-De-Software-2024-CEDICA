from flask import Blueprint, flash, redirect, render_template, Request, request, url_for

from src.core import adressing, people, professions
from web.forms.member_form import MemberForm

bp = Blueprint("team", __name__, url_prefix ="/team") 

@bp.get("/")
def index()->str:
    """Listado de miembros del equipo"""
    members = people.list_members()
    return render_template('team/index.html', members=members)

@bp.get("/<int:id>")
def show(id: int)->str:
    """Detalle de un miembro del equipo"""
    member = people.get_member_by_field('id', id)
    return render_template('team/show.html', member=member)

def _get_data_from_db():
    """Obtiene los datos de la base de datos"""
    profession_list = professions.list_professions()
    jobs = professions.list_jobs()
    provinces = adressing.list_provinces()
    localities = adressing.list_localities()
    return profession_list, jobs, provinces, localities

def _get_validator(profession_list:list, jobs:list, localities:list, member_id=None)->MemberForm:
    """Configura los campos del formulario"""
    form = MemberForm(member_id=member_id)
    form.profession_id.choices = [(profession.id, profession.name) for profession in profession_list]
    form.job_id.choices = [(job.id, job.name) for job in jobs]
    form.locality_id.choices = [(locality.id, locality.name) for locality in localities]
    return form

def _get_form(req:Request, profession_list:list, jobs:list, provinces:list, localities: list, member_id=None)->tuple:
    """Valida los datos del formulario"""
    form = _get_validator(profession_list, jobs, localities, member_id)
    form.process(req.form)
    if not form.validate():
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        flash(f"Error en el formulario -> {'; '.join(error_messages)}", "danger")
        return form, False
    
    return form, True

@bp.route("/new" , methods=['GET', 'POST'])
def create()->str:
    """Formulario para crear un nuevo miembro del equipo"""
    member = {}
    profession_list, jobs, provinces, localities = _get_data_from_db()
    
    # Si se envia el formulario
    if request.method == "POST":
            form, valid = _get_form(request, profession_list, jobs, provinces, localities)
            if valid:
                member = people.member_new(**form.data)
                return redirect(url_for('team.show', id=member.id))
            else:
                member = form.data

    return render_template('team/create.html', member=member, professions=profession_list, jobs=jobs, provinces=provinces, localities=localities)

@bp.route("/<int:id>/edit", methods=['GET', 'POST'])
def update(id: int)->str:
    """Formulario para editar un miembro del equipo"""
    member = people.get_member_by_field('id', id)
    profession_list, jobs, provinces, localities = _get_data_from_db()
    
    # Si se envia el formulario
    if request.method == "POST":
        form, valid = _get_form(request, profession_list, jobs, provinces, localities, member_id=member.id)
        if valid:
            member = people.member_update(id, **form.data)
            return redirect(url_for('team.show', id=member.id))
        else:
            member = form.data
    
    return render_template('team/update.html', member=member, professions=profession_list, jobs=jobs, provinces=provinces, localities=localities)

@bp.post("/<int:id>/delete")
def destroy(id: int)->str:
    """Eliminar un miembro del equipo"""
    member = people.member_delete(id)
    flash(f"El miembro {member.name} {member.last_name} ha sido eliminado", "success")
    return redirect(url_for('team.index'))
