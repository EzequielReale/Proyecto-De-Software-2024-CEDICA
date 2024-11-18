from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField
from src.core.messages.message_status_enum import MessageStatus
from marshmallow import post_dump


class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=100))
    email = fields.Email(required=True, validate=validate.Length(max=100))
    description = fields.Str(required=True, validate=validate.Length(max=400))
    status = EnumField(MessageStatus, by_value=True, required=False,missing=MessageStatus.CREATED.value)
    comment = fields.Str(validate=validate.Length(max=400),allow_none=True)
    created_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%SZ')
    closed_at = fields.DateTime(allow_none=True,format='%Y-%m-%dT%H:%M:%SZ')


    class Meta:
        ordered = True

class MessageResponseSchema(Schema):
    title = fields.Str(attribute="name")  
    email = fields.Email()
    description = fields.Str(attribute="body_message")  
    status=fields.Method("get_status",attribute="state")
    created_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%SZ')
    closed_at = fields.DateTime(allow_none=True, format='%Y-%m-%dT%H:%M:%SZ')


    def get_status(self,obj):
        return obj.state.value

message_response= MessageResponseSchema()
message_schema = MessageSchema()
