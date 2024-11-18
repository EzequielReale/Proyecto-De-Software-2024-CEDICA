from marshmallow import Schema, fields, validate, ValidationError

class MessageSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    status = fields.Str(required=False, validate=validate.OneOf(['created', 'closed']))
    created_at = fields.DateTime(required=False)  # Validación de formato de fecha
    closed_at = fields.DateTime(required=False)   # Validación de formato de fecha

# Crear una instancia del esquema para validar múltiples mensajes si es necesario
message_schema = MessageSchema()
