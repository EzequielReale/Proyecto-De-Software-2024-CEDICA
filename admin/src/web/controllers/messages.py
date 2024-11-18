from flask import (
    Blueprint,
    render_template,
    session,
    request,
    flash,
    redirect,
)

from src.core.messages.message import Message
from src.core.messages.message_status_enum import MessageStatus
from src.core import database_functions as dbf
from src.web.handlers.autenticacion import check_permission, login_required
from src.web.handlers.error import unauthorized

bp = Blueprint("internal_messages", __name__, url_prefix="/messages")


@bp.get("/")
@login_required
def index() -> str:
    """Listado de mensajes usando filtros, ordenación y paginación"""
    if not check_permission(session,"message_index"):
        return unauthorized()
    
    # Obtiene página
    page = request.args.get('page', 1, type=int)
    per_page = 25

    # Obtener los filtros de búsqueda y ordenación
    filters = {
        "state": request.args.get("state"),
    }

    sort_by = request.args.get("sort_by", "created_at")
    sort_direction = request.args.get("sort_direction", "asc")

    messages, total_pages = dbf.list_paginated(
        Message, filters, page, per_page, sort_by, sort_direction
    )

    return render_template(
        "messages/index.html",
        messages=messages,
        message_status=MessageStatus,
        page=page,
        total_pages=total_pages,
        filters=filters,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )


@bp.get("/<int:id>")
@login_required
def show(id: int) -> str:
    """Recibe el id de un mensaje y muestra su información"""
    if not check_permission(session,"message_show"):
        return unauthorized()
    message = dbf.get_by_field(Message, 'id', id)
    return render_template('messages/show.html', message=message, message_status=MessageStatus)
    


@bp.post("/update/<int:id>")
@login_required
def update(id: int) -> str:
    """Recibe el id de un mensaje y actualiza su estado"""
    if not check_permission(session,"message_update"):
        return unauthorized()
    
    message = dbf.get_by_field(Message, 'id', id)

    if message is None:
        flash('El mensaje no existe', 'danger')
        return redirect("/messages")

    state = request.form.get('state')

    # Falta chequear que sea un estado valido

    dbf.update(Message, message.id, state=state)
    flash('Estado del mensaje actualizado correctamente', 'success')
    return render_template('messages/show.html', message=message, message_status=MessageStatus)



@bp.post("/delete/<int:id>")
@login_required
def delete(id: int) -> str:
    """Recibe el id de un mensaje y lo elimina"""
    if not check_permission(session,"message_destroy"):
        return unauthorized()
    
    if (dbf.get_by_field(Message, 'id', id) is not None):
        dbf.delete(Message, id)
        flash('Mensaje borrado correctamente', 'success')
        return redirect("/messages")
    else:
        flash('El mensaje que desea borrar no existe', 'danger')
        return redirect("/messages")


# Agrego más permisos? o agrego esta logica a update?

@bp.post("/<int:id>/add_comment")
@login_required
def add_comment(id: int) -> str:
    """Recibe el id de un mensaje y le agrega un comentario"""
    if not check_permission(session,"message_show"):
        return unauthorized()
    
    message = dbf.get_by_field(Message, 'id', id)

    if message is None:
        flash('El mensaje no existe', 'danger')
        return redirect("/messages")
    
    new_comment = request.form.get('comment')

    if new_comment:

        if _comment_has_valid_length(new_comment):
            dbf.update(Message, message.id, comment=new_comment)
            flash('Se agrego el comentario con exito', 'success')
            return render_template('messages/show.html', message=message, message_status=MessageStatus)
        else:
            flash('El comentario no puede superar los 400 caracteres', 'danger')
            return render_template('messages/show.html', message=message, message_status=MessageStatus)
            
    
    else:
        flash('El comentario no puede estar vacio', 'danger')
        return render_template('messages/show.html', message=message, message_status=MessageStatus)


@bp.post("/<int:id>/delete_comment")
@login_required
def destroy_comment(id: int) -> str:
    """Recibe el id de un mensaje y edita su comentario"""
    if not check_permission(session,"message_show"):
        return unauthorized()
    
    message = dbf.get_by_field(Message, 'id', id)

    if message is None:
        flash('El mensaje no existe', 'danger')
        return redirect("/messages")
    
    result = dbf.update(Message, message.id, comment=None)
    if (result):
        flash('Se borro el comentario con exito', 'success')
        return render_template('messages/show.html', message=message, message_status=MessageStatus)
    else:
        flash('No se pudo borrar el comentario', 'danger')
        return render_template('messages/show.html', message=message, message_status=MessageStatus)



def _message_has_valid_length(body_message):
    """Valida que el cuerpo del mensaje no supere los 400 caracteres"""
    if len(body_message) > 399:
        return False
    return True

def _comment_has_valid_length(body_message):
    """Valida que el comentario no supere los 400 caracteres"""
    if len(body_message) > 399:
        return False
    return True

def _message_state_is_valid(message_state):
    """Valida que el estado ingresado sea un estado valido"""
    