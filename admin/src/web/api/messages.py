from flask import Flask, request, jsonify,Blueprint 
from src.web.schemas.messages import message_schema


bp= Blueprint("messages",__name__,url_prefix="/api/messages")


@bp.post("/")
def create_message():
    data = request.get_json()
    error = message_schema.validate(data)
    if error:
        return jsonify({"error": "Parámetros inválidos o faltantes en la solicitud."}), 400
    else: #{
        new_message = Message( #no se como se llama el modelo , todavia no esta
            title=data['title'],
            email=data['email'],
            description=data['description'],
            status=data.get('status', 'created'),
            created_at=data.get('created_at', db.func.current_timestamp()),
            closed_at=data.get('closed_at', None)
        )

    # aca tengo que llamar a la funcion de init core de contacto
        db.session.add(new_message)
        db.session.commit()
        #} tod esto es una funcion del modelo 

        result = message_schema.dump(new_message)

        return jsonify(result), 201
