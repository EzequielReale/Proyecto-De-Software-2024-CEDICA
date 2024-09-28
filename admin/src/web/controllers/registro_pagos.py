from flask import Blueprint
from flask import render_template
from flask import request,redirect, flash,url_for

from flask import session
from src.core import registro_pagos
from src.core import auth


bp= Blueprint("registro_pagos",__name__,url_prefix="/registro_pagos")

@bp.get("/")
def index():
    """controlador listado, paso al template los pagos"""
    pagos = registro_pagos.administracion_index()
    return render_template("registro_pagos/index.html",pagos=pagos)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """controlador para actualizar un pago"""
    exito = registro_pagos.administracion_update(request,id)
    if exito:
        flash('Pago actualizado exitosamente.', 'success')
        return redirect(url_for('registro_pagos.index')) 
    else:
         #es la primera vez q entra o hubo algun error en el envio
         tipos = registro_pagos.administracion_tipoPagos()
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
     pude = registro_pagos.administracion_create(request)
     if pude:
         flash('Se agrego el pago correctamente.', 'success')
         return redirect(url_for('registro_pagos.index')) 
     else:
       #es l primera vez q entra o hubo un problema con el envio
       return render_template('registro_pagos/creacion.html', tipos= registro_pagos.administracion_tipoPagos(),users= auth.list_users()) 