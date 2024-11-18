from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField
from src.core.messages.message_status_enum import MessageStatus

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=100))
    email = fields.Email(required=True, validate=validate.Length(max=100))
    description = fields.Str(required=True, validate=validate.Length(max=400))
    status = EnumField(MessageStatus, by_value=True, required=False,missing='CREATED')
    comment = fields.Str(validate=validate.Length(max=400),allow_none=True)
    created_at = fields.DateTime()
    closed_at = fields.DateTime(allow_none=True)


    class Meta:
        ordered = True

message_schema = MessageSchema()
