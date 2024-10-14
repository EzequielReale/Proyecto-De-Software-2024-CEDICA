from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.core.people.member_rider import Member
from src.core.people.tutor import Tutor
from src.core.professions.school import School
from src.core.professions.job_proposal import JobProposal
from src.core.equestrian.horse import Horse
from src.core import adressing, disabilities, people, professions
from src.web.forms.person_document_form import PersonDocumentForm as DocumentForm
from src.web.forms.person_link_form import PersonLinkForm as LinkForm
from src.web.forms.rider_form import RiderForm
from src.web.handlers.autenticacion import login_required


bp = Blueprint("jya", __name__, url_prefix="/jya")


@bp.get("/")
@login_required
def index() -> str:
    """Listado de j/a del equipo usando filtros, ordenación y paginación"""
    page = request.args.get("page", 1, type=int)
    per_page = 25

    # Obtener los filtros de búsqueda y ordenación
    filters = {
        "name": request.args.get("name"),
        "last_name": request.args.get("last_name"),
        "dni": request.args.get("dni"),
        "members": request.args.getlist("members", type=int),
    }
    
    sort_by = request.args.get("sort_by", "name")
    sort_direction = request.args.get("sort_direction", "asc")

    riders, total_pages = people.list_riders(
        filters, page, per_page, sort_by, sort_direction
    )
    return render_template(
        "jya/index.html",
        riders=riders,
        members=people.list_professionals(),
        filters=filters,
        page=page,
        total_pages=total_pages,
        sort_by=sort_by,
        sort_direction=sort_direction,
        current_year=datetime.now().year,
    )


@bp.get("/<int:id>")
@login_required
def show(id: int) -> str:
    """Recibe el id de un j/a y muestra su información y documentos asociados"""
    filters = {
        "document_name": request.args.get("document_name"),
        "document_type": request.args.get("document_type"),
        "person_id": id,
    }
    sort_by = request.args.get("sort_by", "document_name")
    sort_direction = request.args.get("sort_direction", "asc")
    rider = people.get_rider_by_field("id", id)
    documents = people.list_filtered_documents(id, filters, sort_by, sort_direction) 
    return render_template("jya/show.html", rider=rider, documents=documents, filters=filters, sort_by=sort_by, sort_direction=sort_direction, current_year=datetime.now().year,)


def _get_data_from_db() -> tuple:
    """Obtiene la lista de discapacidades, tipos de discapacidades, provincias, localidades y miembros del equipo"""
    disability_types_list = disabilities.list_disability_types()
    disabilities_list = disabilities.list_disability_diagnosis()
    localities_list = adressing.list_localities()
    provinces_list = adressing.list_provinces()
    horse_list = Horse.query.all()
    member_list = Member.query.all()
    return disability_types_list, disabilities_list, provinces_list, localities_list, member_list, horse_list


def _configure_form(disability_types_list:list, disabilities_list:list, provinces_list:list, localities_list:list, member_list:list, horse_list:list, rider_id:int=None) -> RiderForm:
    """Recibe la lista de profesiones, trabajos, localidades y el id del j/a y retorna el validador del formulario"""
    form = RiderForm(rider_id=rider_id)
    form.province_of_birth.choices = [(province.id, province.name) for province in provinces_list]
    form.city_of_birth.choices = [(locality.id, locality.name) for locality in localities_list]
    form.province_id.choices = [(province.id, province.name) for province in provinces_list]
    form.locality_id.choices = [(locality.id, locality.name) for locality in localities_list]    
    form.disability_type.choices = [(disability_type.id, disability_type.name) for disability_type in disability_types_list]
    form.disability_id.choices = [(disability.id, disability.name) for disability in disabilities_list]
    form.assigned_professionals.choices = [(member.id, member.name, member.last_name) for member in member_list]
    form.professor_id.choices = [(member.id, member.name, member.last_name) for member in member_list]
    form.assistant_id.choices = [(member.id, member.name, member.last_name) for member in member_list]
    return form


def _create_rider(form:RiderForm) -> int:
    """Recibe el formulario y retorna el id del j/a creado"""
    tutor_1, tutor_2 = _create_tutors(form)
    rider_data = form.get_rider_data()
    rider_data['locality'] = adressing.get_locality_by_id(rider_data['locality_id'])
    rider_data['city_of_birth'] = adressing.get_locality_by_id(rider_data['city_of_birth'])
    rider_data['tutor_1'] = tutor_1 if tutor_1 else None
    rider_data['tutor_2'] = tutor_2 if tutor_2 else None
    member_ids = form.assigned_professionals.data
    rider_data['members'] = [people.get_member_by_field("id", member_id) for member_id in member_ids]

    return people.rider_new(**rider_data)


def _create_tutors(form:RiderForm) -> int:
    """Recibe el formulario y el número de tutor y retorna el id del tutor creado"""
    tutor_1 = None
    tutor_2 = None

    if form.has_tutor_1.data == "True":
        tutor_1 = people.tutor_new(**form.get_tutor_data(1))
    if form.has_tutor_2.data == "True":
        tutor_2 = people.tutor_new(**form.get_tutor_data(2))
    return tutor_1, tutor_2


def _create_school(form:RiderForm, rider_id:int) -> int:
    """Recibe el formulario y el id del j/a y retorna el id de la escuela creada"""
    school = School()
    if form.has_school.data == "True":
        school = professions.school_new(**form.get_school_data(), rider_id=rider_id)
    return school.id


def _create_job_proposal(form:RiderForm, rider_id:int) -> int:
    """Recibe el formulario y el id del j/a y retorna el id de la propuesta de trabajo creada"""
    job_proposal = JobProposal()
    if form.has_job_proposal.data == "True":
        job_proposal = professions.job_proposal_new(**form.get_job_proposal_data(), rider_id=rider_id)
    return job_proposal.id


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create() -> str:
    """Muestra el formulario para crear un nuevo j/a y lo guarda en la BD"""
    rider = {}
    disability_types_list, disabilities_list, provinces_list, localities_list, member_list, horse_list = _get_data_from_db()
    form = _configure_form(disability_types_list, disabilities_list, provinces_list, localities_list, member_list, horse_list)

    # Si se envia el formulario
    if form.validate_on_submit():
        rider = _create_rider(form)
        _create_school(form, rider.id)
        _create_job_proposal(form, rider.id)
        flash(f"{rider.name} {rider.last_name} ha sido creado exitosamente", "success")
        return redirect(url_for("jya.show", id=rider.id))
    elif form.errors:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        flash(f"Error en el formulario: {error_messages}", "danger")
        rider = {field.name: field.data for field in form}

    return render_template(
        "jya/create.html",
        rider=rider,
        disability_types=disability_types_list,
        disabilities=disabilities_list,
        localities=localities_list,
        provinces=provinces_list,
        members=member_list,
        horses=horse_list,
        csrf_token=(form.csrf_token if hasattr(form, 'csrf_token') else None)
    )


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def update(id: int) -> str:
    """Recibe el id de un j/a y muestra el formulario para editarlo, al mismo tiempo que lo actualiza en la BD"""
    rider = people.get_rider_by_field("id", id)

    # Para después

    return render_template(
        "jya/update.html",
        rider=rider,
    )


@bp.post("/<int:id>/delete")
@login_required
def destroy(id: int) -> str:
    """Recibe el id de un j/a y lo elimina fisicamente de la BD"""
    rider = people.get_rider_by_field("id", id)

    documents = people.list_documents(rider.id)
    for document in documents:
        people.delete_document(document["id"])

    if rider.tutor_1:
        people.tutor_delete(rider.tutor_1.id)
    if rider.tutor_2:
        people.tutor_delete(rider.tutor_2.id)
    if rider.school:
        for school in rider.school:
            professions.school_delete(school.id)
    if rider.job_proposal:
        for job_proposal in rider.job_proposal:
            professions.job_proposal_delete(job_proposal.id)

    rider = people.rider_delete(id)
    flash(f"{rider.name} {rider.last_name} ha sido eliminado", "success")

    return redirect(url_for("jya.index"))


@bp.route("/<int:id>/add_document", methods=["GET", "POST"])
@login_required
def add_document(id: int) -> str:
    """Recibe el id de un j/a y agrega un documento a su lista de documentos"""
    form = DocumentForm()
    if form.validate_on_submit():
        document = form.document.data
        type = form.document_type.data
        people.rider_add_document(id, document, type)
        flash("Documento agregado exitosamente", "success")
        return redirect(url_for("jya.show", id=id))
    elif form.errors:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        flash(f"Error en el formulario: {error_messages}", "danger")

    return render_template("jya/add_document.html", rider_id=id, form=form)


@bp.route("/<int:id>/add_link", methods=["GET", "POST"])
@login_required
def add_link(id: int) -> str:
    """Recibe el id de un j/a y agrega un enlace a su lista de documentos"""
    form = LinkForm()
    if form.validate_on_submit():
        name = form.document_name.data
        path = form.document_path.data
        type = form.document_type.data
        people.document_new(id, path, name, type, link=True)
        flash("Enlace cargado exitosamente", "success")
        return redirect(url_for("jya.show", id=id))
    elif form.errors:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        flash(f"Error en el formulario: {error_messages}", "danger")

    return render_template("jya/add_link.html", rider_id=id, form=form)


@bp.post("/<int:id>/delete_document/<int:document_id>")
@login_required
def destroy_document(id: int, document_id: int) -> str:
    """Recibe el id de un j/a y el id de un documento y lo elimina de la BD"""
    document = people.delete_document(document_id)
    flash(f"Documento {document.document_name} eliminado exitosamente", "success")
    return redirect(url_for("jya.show", id=id))
