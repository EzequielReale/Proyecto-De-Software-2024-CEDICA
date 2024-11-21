from flask import  request, jsonify,Blueprint 
from src.web.schemas.messages import message_schema
from src.web.schemas.messages import message_response

from src.core.messages.message import Message
from src.core.messages.message_status_enum import MessageStatus
from src.core import database_functions as dbf
from datetime import datetime


bp= Blueprint("messages_api",__name__,url_prefix="/api")


@bp.post("/messages")
def create_message():
    data = request.get_json()
    error = message_schema.validate(data)
    if error:
        return jsonify({"error": "Parámetros inválidos o faltantes en la solicitud."}), 400

    status_value = data.get('status', 'No respondido')
    status_enum = MessageStatus(status_value)
    message_data = {
        'name': data['title'],
        'email': data['email'],
        'body_message': data['description'],
        'state': status_enum,
        'created_at': data.get('created_at', datetime.now().isoformat() + 'Z'),
        'closed_at': data.get('closed_at', None),
        'comment': data.get('comment', None)
    }
    new_message = dbf.new(Message, **message_data)

    result = message_response.dump(new_message)
    return jsonify(result), 201