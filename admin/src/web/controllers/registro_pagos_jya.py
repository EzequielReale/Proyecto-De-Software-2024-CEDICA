from flask import Blueprint
from flask import session
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import redirect

# Importo Modelos
from src.core.registro_pagos_jya.pagos_jya import PagoJineteAmazona
from src.core.registro_pagos_jya.pagos_jya import MediosDePago
from src.core.people.member_rider import Rider
from src.core.people.member_rider import Member

# Importo formularios
from src.web.forms.jya_payment_register_form import RegisterJyAPaymentForm
from src.web.forms.jya_payment_update_form import UpdateJyaAParmentForm

# Importo funciones
from src.core.registro_pagos_jya import get_medio_de_pago
from src.core.registro_pagos_jya import get_pago_jya
from src.core.registro_pagos_jya import list_paginated
from src.core.registro_pagos_jya import pago_jya_delete
from src.core.registro_pagos_jya import pago_jya_new
from src.core.registro_pagos_jya import pago_jya_update
from src.core.database_functions import list_all
from src.core.people import get_member_by_field, get_rider_by_field


from src.web.handlers.autenticacion import login_required
from src.web.handlers.autenticacion import check_permission
from src.web.handlers.error import unauthorized

bp = Blueprint("registro_pagos_jya", __name__, url_prefix="/registro_pagos_jya")


@login_required
@bp.get("/")
def index():
    """Lista los pagos de Jinetes y Amazonas"""
    if not check_permission(session, "reg_cobros_index"):
        return unauthorized()

    page = request.args.get("page", 1, type=int)
    per_page = 25

    # Obtener los filtros de búsqueda y ordenación
    filters = {
        "fecha_inicio": request.args.get("fecha_inicio"),
        "fecha_fin": request.args.get("fecha_fin"),
        "medio_de_pago": request.args.get("medio_de_pago"),
        "receptor_name": request.args.get("nombre_receptor"),
        "receptor_last_name": request.args.get("apellido_receptor"),
    }

    sort_by = request.args.get("sort_by", "fecha_pago")
    sort_direction = request.args.get("sort_direction", "asc")

    pagos, total_pages = list_paginated(
        PagoJineteAmazona, filters, page, per_page, sort_by, sort_direction
    )

    return render_template(
        "registro_pagos_jya/index.html",
        pagos=pagos,
        medios_de_pago=list_all(MediosDePago),
        filters=filters,
        page=page,
        total_pages=total_pages,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )


@bp.route("/create", methods=["GET", "POST"])
def create():
    """Formulario para registrar un nuevo cobro"""
    if not check_permission(session, "reg_cobros_new"):
        return unauthorized()

    form = RegisterJyAPaymentForm()

    riders_choices = [
        (rider.id, rider.last_name + " " + rider.name) for rider in list_all(Rider)
    ]
    form.jya.choices = [("", "Seleccione una opción")] + riders_choices

    members_choices = [
        (member.id, member.last_name + " " + member.name) for member in list_all(Member)
    ]
    form.receptor.choices = [("", "Seleccione una opción")] + members_choices

    medios_de_pago_choices = [
        (medio.id, medio.tipo) for medio in list_all(MediosDePago)
    ]
    form.medio_de_pago.choices = [
        ("", "Seleccione una opción")
    ] + medios_de_pago_choices

    if form.validate_on_submit():

        jinete_amazona = form.jya.data
        medio_de_pago = form.medio_de_pago.data
        fecha_pago = form.fecha_pago.data
        monto = form.monto_pago.data
        receptor = form.receptor.data
        en_deuda = form.estado_de_pago.data
        observaciones = form.observaciones.data

        # A partir de los valores recibidos en el form, transformo los valores para poder crear el pago

        medio_de_pago = get_medio_de_pago(medio_de_pago)
        jinete_amazona = get_rider_by_field("id", jinete_amazona)
        receptor = get_member_by_field("id", receptor)
        en_deuda = True if en_deuda == "1" else False

        new_payment = pago_jya_new(
            jinete_amazona=jinete_amazona,
            medio_de_pago=medio_de_pago,
            fecha_pago=fecha_pago,
            monto=monto,
            receptor=receptor,
            en_deuda=en_deuda,
            observaciones=observaciones,
        )

        if new_payment:
            flash("Pago registrado exitosamente", "success")
            return redirect("/registro_pagos_jya")
        else:
            flash("Ocurrio un error al registrar el pago", "danger")
            return redirect("/registro_pagos_jya")

    return render_template(
        "registro_pagos_jya/create.html",
        form=form,
        csrf_token=(form.csrf_token if hasattr(form, "csrf_token") else None),
    )


@login_required
@bp.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if not check_permission(session, "reg_cobros_update"):
        return unauthorized()

    payment = get_pago_jya(id)

    form = UpdateJyaAParmentForm(obj=payment)

    # Cargo las opciones posibles excluyendo los valores que ya estan seteados en el pago

    riders_choices = [
        (rider.id, rider.last_name + " " + rider.name)
        for rider in list_all(Rider)
        if rider.id != id
    ]
    form.jinete_amazona.choices = [("", "Seleccione una opción")] + riders_choices

    members_choices = [
        (member.id, member.last_name + " " + member.name)
        for member in list_all(Member)
        if member.id != payment.receptor_id
    ]
    form.receptor.choices = [("", "Seleccione una opción")] + members_choices

    medios_de_pago_choices = [
        (medio.id, medio.tipo)
        for medio in list_all(MediosDePago)
        if medio.id != payment.medio_de_pago_id
    ]
    form.medio_de_pago.choices = [
        ("", "Seleccione una opción")
    ] + medios_de_pago_choices

    if payment.en_deuda:
        estado_de_pago_choices = [(0, "Pagado")]
    else:
        estado_de_pago_choices = [(1, "En deuda")]

    form.estado_de_pago.choices = [
        ("", "Seleccione una opción")
    ] + estado_de_pago_choices

    if form.validate_on_submit():

        jinete_amazona = form.jinete_amazona.data
        medio_de_pago = form.medio_de_pago.data
        fecha_pago = form.fecha_pago.data
        monto = form.monto.data
        receptor = form.receptor.data
        en_deuda = form.estado_de_pago.data
        observaciones = form.observaciones.data

        fields_to_change = {}

        if jinete_amazona != "":
            jinete_amazona = get_rider_by_field("id", jinete_amazona)
            fields_to_change["jinete_amazona"] = jinete_amazona

        if medio_de_pago != "":
            medio_de_pago = get_medio_de_pago(medio_de_pago)
            fields_to_change["medio_de_pago"] = medio_de_pago

        if fecha_pago != "":
            fields_to_change["fecha_pago"] = fecha_pago

        if monto != "":
            fields_to_change["monto"] = monto

        if receptor != "":
            receptor = get_member_by_field("id", receptor)
            fields_to_change["receptor"] = receptor

        if en_deuda != "":
            en_deuda = True if en_deuda == "1" else False
            fields_to_change["en_deuda"] = en_deuda

        if observaciones != "":
            fields_to_change["observaciones"] = observaciones

        pago_jya_update(id, **fields_to_change)

        flash("Pago actualizado exitosamente", "success")
        return redirect("/registro_pagos_jya")

    return render_template(
        "registro_pagos_jya/update.html",
        payment=payment,
        form=form,
        csrf_token=(form.csrf_token if hasattr(form, "csrf_token") else None),
    )


@bp.route("/destroy/<int:id>", methods=["POST"])
def destroy(id):
    if not check_permission(session, "reg_cobros_destroy"):
        return unauthorized()

    pago_jya_delete(id)
    flash("Pago eliminado exitosamente", "success")
    return redirect("/registro_pagos_jya")
