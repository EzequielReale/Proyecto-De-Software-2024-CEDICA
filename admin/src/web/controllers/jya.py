from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.core.people.member_rider import Member
from src.core.equestrian.horse import Horse
from src.core import adressing, disabilities, people, professions, database_functions as db
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
        members=db.filter(Member, {'job_id': 2}), # Terapeutas
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
    horse_list = Horse.query.all() # Hago una funcion en init para esto?
    assigned_professionals_list = db.filter(Member, {"job_id": 2}) # Terapeuta
    professor_list = db.filter(Member, {"job_id": 9}) # Profesor de equitación
    professor_list = list(professor_list) + list(assigned_professionals_list)
    assistant_list = db.filter(Member, {"job_id": 4}) # Asistente de pista
    horse_rider_list = db.filter(Member, {"job_id": 3}) # Conductor
    return disability_types_list, disabilities_list, provinces_list, localities_list, assigned_professionals_list, professor_list, assistant_list, horse_rider_list, horse_list


def _configure_form(disability_types_list:list, disabilities_list:list, provinces_list:list, localities_list:list, assigned_professionals_list:list, professor_list:list, assistant_list:list, horse_rider_list:list, horse_list:list, rider_id:int=None) -> RiderForm:
    """Recibe la lista de profesiones, trabajos, localidades y el id del j/a y retorna el validador del formulario"""
    form = RiderForm(rider_id=rider_id)
    form.province_of_birth.choices = [(province.id, province.name) for province in provinces_list]
    form.city_of_birth.choices = [(locality.id, locality.name) for locality in localities_list]
    form.province_id.choices = [(province.id, province.name) for province in provinces_list]
    form.locality_id.choices = [(locality.id, locality.name) for locality in localities_list]    
    form.disability_type.choices = [(disability_type.id, disability_type.name) for disability_type in disability_types_list]
    form.disability_id.choices = [(disability.id, disability.name) for disability in disabilities_list]
    form.assigned_professionals.choices = [(member.id, member.name, member.last_name) for member in assigned_professionals_list]
    form.professor_id.choices = [(member.id, member.name, member.last_name) for member in professor_list]
    form.assistant_id.choices = [(member.id, member.name, member.last_name) for member in assistant_list]
    form.member_horse_rider_id.choices = [(member.id, member.name, member.last_name) for member in horse_rider_list]
    form.horse_id.choices = [(horse.id, horse.name) for horse in horse_list]
    return form


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create() -> str:
    """Muestra el formulario para crear un nuevo j/a y lo guarda en la BD"""
    rider = {}
    disability_types_list, disabilities_list, provinces_list, localities_list, assigned_professionals_list, professor_list, assistant_list, horse_rider_list, horse_list = _get_data_from_db()
    form = _configure_form(disability_types_list, disabilities_list, provinces_list, localities_list, assigned_professionals_list, professor_list, assistant_list, horse_rider_list, horse_list)

    # Si se envia el formulario
    if form.validate_on_submit():
        rider = people.rider_new(form)
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
        assigned_professionals=assigned_professionals_list,
        professors=professor_list,
        assistants=assistant_list,
        horse_riders=horse_rider_list,
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
    rider = people.rider_delete(id)
    flash(f"{rider.name} {rider.last_name} ha sido eliminado", "success")
    return redirect(url_for("jya.index"))


@bp.route("/<int:id>/add_document", methods=["GET", "POST"])
@login_required
def add_document(id: int) -> str:
    """Recibe el id de un j/a y agrega un documento a su lista de documentos"""
    form = DocumentForm()
    if form.validate_on_submit():
        document, type = form.get_data()
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
        name, path, type = form.get_data()
        people.document_new(id, path, name, type, link=True)
        flash("Enlace cargado exitosamente", "success")
        return redirect(url_for("jya.show", id=id))
    elif form.errors:
        error_messages = [f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()]
        flash(f"Error en el formulario: {error_messages}", "danger")

    return render_template("jya/add_link.html", rider_id=id, form=form)


@bp.get("/<int:id>/download_document/<int:document_id>")
@login_required
def download_document(id: int, document_id: int) -> bytes:
    """Recibe el id de un j/a y el id de un documento y lo descarga"""
    return people.download_document(document_id)


@bp.post("/<int:id>/delete_document/<int:document_id>")
@login_required
def destroy_document(id: int, document_id: int) -> str:
    """Recibe el id de un j/a y el id de un documento y lo elimina de la BD"""
    document = people.delete_document(document_id)
    flash(f"Documento {document.document_name} eliminado exitosamente", "success")
    return redirect(url_for("jya.show", id=id))
