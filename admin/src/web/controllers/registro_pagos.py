from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.core import registro_pagos, people, database_functions as db
from src.web.handlers.autenticacion import check_permission
from src.web.handlers.error import unauthorized
from src.web.handlers.autenticacion import login_required

bp= Blueprint("registro_pagos",__name__,url_prefix="/registro_pagos")

@login_required
@bp.get("/")
def index():
    """controlador listado, paso al template los pagos"""
    if  not check_permission(session,"reg_pagos_index"):
         return unauthorized()
    pagos = registro_pagos.administracion_index(request)
    return render_template("registro_pagos/index.html",pagos=pagos)


#saco los flash para que sea mas generica 
def validar(monto, tipo_pago_id, fecha_pago, des, beneficiario_id):
    """Valido los parámetros según ciertos requerimientos"""
    
    
    if not monto or float(monto) <= 0:
        return False, "El monto debe ser mayor a 0", None, None
    
    
    if not tipo_pago_id:
        return False, "Debe seleccionar un tipo de pago", None, None
    
    
    if not fecha_pago:
        return False, "Debe ingresar una fecha de pago", None, None
    
    if fecha_pago > datetime.now().strftime('%Y-%m-%d'):
        return False, "La fecha de pago no puede ser futura", None, None
    
    if not des or len(des) > 255:
        return False, "La descripción es obligatoria y debe tener un máximo de 255 caracteres", None, None
    
    tipo_pago_obj = registro_pagos.get_tipo_pago(tipo_pago_id)
    if not tipo_pago_obj:
        return False, "El tipo de pago seleccionado no es válido", None, None
    
    beneficiario = None


    if beneficiario_id:
        beneficiario = people.get_member_by_field('id', beneficiario_id)
        if not beneficiario:
            return False, "El beneficiario seleccionado no es válido", None, None
    
    return True, "", beneficiario, tipo_pago_obj


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
    #es la primera vez q entra o hubo algun error en el envio
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
        
        pude,mensaje,beneficiario,tipo_pago =validar(monto,tipo_pago_id,fecha_pago,des,beneficiario_id)
        if pude:
             if(beneficiario):
                pago_data = {
                'beneficiario': beneficiario,
                'monto': monto,
                'tipo_pago': tipo_pago,
                'fecha_pago': fecha_pago,
                'descripcion': des
             }
             else:
                  pago_data = {
                'monto': monto,
                'tipo_pago': tipo_pago,
                'fecha_pago': fecha_pago,
                'descripcion': des
             }

             registro_pagos.administracion_create(**pago_data)
             flash('Se agrego el pago correctamente.', 'success')
             return redirect(url_for('registro_pagos.index')) 
        else:
            flash(mensaje, 'danger')
       #es l primera vez q entra o hubo un problema con el envio
     return render_template('registro_pagos/creacion.html', tipos= registro_pagos.administracion_tipoPagos(),users= list_users()) 