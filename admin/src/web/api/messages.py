from flask import Flask, request, jsonify,Blueprint 
from src.web.schemas.messages import message_schema
from src.web.schemas.messages import message_response

from src.core.messages.message import Message
from src.core.messages.message_status_enum import MessageStatus
from datetime import datetime
from src.core.database import db


bp= Blueprint("messages_api",__name__,url_prefix="/api")


@bp.post("/messages")
def create_message():
    data = request.get_json()
    error = message_schema.validate(data)
    if error:
        print("Errores de validación:", error)  # Imprime los errores para ver qué está fallando

        return jsonify({"error": "Parámetros inválidos o faltantes en la solicitud."}), 400


    status_value = data.get('status', 'No respondido')
    status_enum = MessageStatus(status_value)

    new_message = Message(
        name=data['title'],
        email=data['email'],
        body_message=data['description'],
        state=status_enum,
        created_at=data.get('created_at', datetime.utcnow().isoformat() + 'Z'),
        closed_at=data.get('closed_at', None),
        comment=data.get('comment', None)
    )
    db.session.add(new_message)
    db.session.commit()

    result = message_response.dump(new_message)
    return jsonify(result), 201