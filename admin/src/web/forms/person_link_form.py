from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, SubmitField

from src.core import people


class PersonLinkForm(FlaskForm):


    def __init__(self, document_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document_id = document_id


    document_name = StringField('Nombre', [validators.DataRequired()])
    document_path = StringField('URL', [
        validators.DataRequired(),
        validators.URL(message='Debe ser una URL válida'),
        validators.Regexp(
            r'^(https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(/[^\s]*)?$',
            message='La URL debe tener un formato válido (ej: https://example.com/path)'
        )
    ])
    document_type = SelectField('Tipo de documento', choices=[
        ('Entrevista', 'Entrevista'),
        ('Evaluación', 'Evaluación'),
        ('Planificaciones', 'Planificaciones'),
        ('Evolución', 'Evolución'),
        ('Crónicas', 'Crónicas'),
        ('Documental', 'Documental')
    ], validators=[validators.Optional()])
    submit = SubmitField('Guardar')


    def validate_document_name(self, field):
        """Valida que el nombre del documento sea único, excluyendo el documento actual si se está editando"""
        id = request.view_args.get('id')
        documents = people.list_documents(id)
        for doc in documents:
            if doc['name'] == field.data and (self.document_id is None or doc['id'] != self.document_id):
                raise validators.ValidationError('El nombre del documento ya existe para esta persona.')

        
    def validate_document_path(self, field):
        """Valida que la URL del documento sea única, excluyendo el documento actual si se está editando"""
        id = request.view_args.get('id')        
        documents = people.list_documents(id)
        for doc in documents:
            if doc['url'] == field.data and (self.document_id is None or doc['id'] != self.document_id):
                raise validators.ValidationError('La URL del documento ya existe para esta persona.')
        
    def get_data(self) -> tuple:
        """Devuelve el nombre, la URL y el tipo de documento"""
        return self.document_name.data, self.document_path.data, self.document_type.data
