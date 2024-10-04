from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.core import auth
from src.core import registro_pagos

bp= Blueprint("registro_pagos",__name__,url_prefix="/registro_pagos")

@bp.get("/")
def index():
    """controlador listado, paso al template los pagos"""
    pagos = registro_pagos.administracion_index(request)
    return render_template("registro_pagos/index.html",pagos=pagos)


def validar(monto,tipo_pago_id,fecha_pago,des,beneficiario_id):
     """valido los parametros segun ciertos requerimientos"""
     if not monto or float(monto) <= 0:
            flash("El monto debe ser mayor a 0", 'danger')
            return False, None,None
        
     if not tipo_pago_id:
         flash("Debe seleccionar un tipo de pago", 'danger')
         return False, None,None
        
     if not fecha_pago:
         flash("Debe ingresar una fecha de pago", 'danger')
         return False, None,None
        
     if not des or len(des) > 255:
         flash("La descripción es obligatoria y debe tener un máximo de 255 caracteres", 'danger')
         return False, None,None
        
        # Verificamos que el tipo de pago exista en la base de datos
     tipo_pago_obj = registro_pagos.get_tipo_pago(tipo_pago_id)
     if not tipo_pago_obj:
         flash("El tipo de pago seleccionado no es válido", 'danger')
         return False, None,None
        
        # Verificamos si se seleccionó un beneficiario
     if beneficiario_id:
         beneficiario = auth.find_user_id(beneficiario_id)
         if not beneficiario:
             flash("El beneficiario seleccionado no es válido", 'danger')
             return False, None,None
     return True, beneficiario,tipo_pago_obj



@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """controlador para actualizar un registro de pago"""
    tipos = registro_pagos.administracion_tipoPagos()

    if request.method == 'POST':
        monto = request.form['monto']
        tipo_pago_id = request.form['tipo_pago'] 
        fecha_pago = request.form['fecha_pago']
        des=  request.form['descripcion']
        beneficiario_id = request.form['beneficiario']
        
        pude,beneficiario,tipo_pago =validar(monto,tipo_pago_id,fecha_pago,des,beneficiario_id)
        if pude:
            registro_pagos.administracion_update(id,monto,tipo_pago,fecha_pago,des,beneficiario)
            flash('Pago actualizado exitosamente.', 'success')
            return redirect(url_for('registro_pagos.index')) 
    #es la primera vez q entra o hubo algun error en el envio
    return render_template('registro_pagos/edicion.html', pago=registro_pagos.administracion_getPago(id), tipos=tipos,users= auth.list_users()) #lo devuelvo al mismo lug con los mismos datos



@bp.route("/destroy/<int:id>", methods=['POST'])
def destroy(id):
     """controlador para eliminar fisicamente un reg de pago"""
     pude = registro_pagos.administracion_destroy(id)
     if(pude):
        flash('Pago eliminado exitosamente.', 'success')
     else:
        flash('Pago no encontrado.', 'danger')

     return redirect(url_for('registro_pagos.index'))



@bp.route("/create", methods=['GET', 'POST'])
def create():
     """controlador para crear un nuevo registro de pago"""
     if request.method == 'POST':
        monto = request.form['monto']
        tipo_pago_id = request.form['tipo_pago'] 
        fecha_pago = request.form['fecha_pago']
        des=  request.form['descripcion']
        beneficiario_id = request.form['beneficiario']
        
        pude,beneficiario,tipo_pago =validar(monto,tipo_pago_id,fecha_pago,des,beneficiario_id)
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
     
       #es l primera vez q entra o hubo un problema con el envio
     return render_template('registro_pagos/creacion.html', tipos= registro_pagos.administracion_tipoPagos(),users= auth.list_users()) 