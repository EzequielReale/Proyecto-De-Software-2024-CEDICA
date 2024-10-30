from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.core import registro_pagos, people, database_functions as db
from src.web.handlers.autenticacion import check_permission
from src.web.handlers.error import unauthorized
from src.web.handlers.autenticacion import login_required
from src.web.forms.registro_pagos_form import validar



bp= Blueprint("registro_pagos",__name__,url_prefix="/registro_pagos")


@login_required
@bp.get("/")
def index():
    """controlador listado, paso al template los pagos"""
    if not check_permission(session, "reg_pagos_index"):
        return unauthorized()
    
    # paginacion
    page = request.args.get("page", 1, type=int)
    per_page = 25

    # filtros
    filtros = {
        "fecha_inicio": request.args.get("fecha_inicio"),
        "fecha_fin": request.args.get("fecha_fin"),
        "tipo_pago": request.args.get("tipo_pago"),
    }

    # orden
    order_by = request.args.get("order_by", "fecha_pago")
    orden = request.args.get("order", "desc")  # por defecto, de más nuevo a más viejo

    pagos, total_paginas = registro_pagos.administracion_index(
        filtros, page, per_page, order_by, orden
    )

    return render_template(
        "registro_pagos/index.html",
        pagos=pagos,
        page=page,
        total_pages=total_paginas,
        filters=filtros,
        sort_by=order_by,
        sort_direction=orden,
    )



@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """controlador para actualizar un registro de pago"""
    if  not check_permission(session,"reg_pagos_update"):
        return unauthorized()
    tipos = registro_pagos.administracion_tipoPagos()

    if request.method == 'POST':
        monto = request.form['monto']
        tipo_pago_id = request.form['tipo_pago'] 
        fecha_pago = request.form['fecha_pago']
        des=  request.form['descripcion']
        beneficiario_id = request.form['beneficiario']
        
        pude,mensaje,beneficiario,tipo_pago =validar(monto,tipo_pago_id,fecha_pago,des,beneficiario_id)
        if pude:
            registro_pagos.administracion_update(id,monto,tipo_pago,fecha_pago,des,beneficiario)
            flash('Pago actualizado exitosamente.', 'success')
            return redirect(url_for('registro_pagos.index')) 
        else:
            flash(mensaje, 'danger')
    return render_template('registro_pagos/edicion.html', pago=registro_pagos.administracion_getPago(id), tipos=tipos,users=db.list_all(people.Member)) #lo devuelvo al mismo lug con los mismos datos


@bp.route("/destroy/<int:id>", methods=['POST'])
def destroy(id):
    """controlador para eliminar fisicamente un reg de pago"""
    if  not check_permission(session,"reg_pagos_destroy"):
        return unauthorized()
    pude = registro_pagos.administracion_destroy(id)
    if(pude):
        flash('Pago eliminado exitosamente.', 'success')
    else:
        flash('Pago no encontrado.', 'danger')

    return redirect(url_for('registro_pagos.index'))


@bp.route("/create", methods=['GET', 'POST'])
def create():
    """controlador para crear un nuevo registro de pago"""
    if  not check_permission(session,"reg_pagos_new"):
        return unauthorized()
    if request.method == 'POST':
        monto = request.form['monto']
        tipo_pago_id = request.form['tipo_pago'] 
        fecha_pago = request.form['fecha_pago']
        des=  request.form['descripcion']
        beneficiario_id = request.form['beneficiario']
            
        pude,mensaje,beneficiario,tipo_pago =registro_pagos_form.validar(monto,tipo_pago_id,fecha_pago,des,beneficiario_id)
        if pude:
            if(beneficiario):
                pago_data = {'beneficiario': beneficiario,'monto': monto,'tipo_pago': tipo_pago,'fecha_pago': fecha_pago,'descripcion': des}
            else:
                pago_data = {'monto': monto,'tipo_pago': tipo_pago,'fecha_pago': fecha_pago,'descripcion': des}
                registro_pagos.administracion_create(**pago_data)
                flash('Se agrego el pago correctamente.', 'success')
                return redirect(url_for('registro_pagos.index')) 
        else:
            flash(mensaje, 'danger')
    return render_template('registro_pagos/creacion.html', tipos= registro_pagos.administracion_tipoPagos(), users=db.list_all(people.Member)) 
