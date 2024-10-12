from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, SubmitField

from src.core import people


class PersonLinkForm(FlaskForm):
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
    ], validators=[validators.DataRequired()])
    submit = SubmitField('Guardar')


    def validate_document_name(self, field):
        """Valida que el nombre del documento sea único"""
        id = request.view_args.get('id')
        if id is None:
            raise validators.ValidationError('ID de la persona no encontrado en la URL.')
        
        documents = people.list_documents(id)
        if any(doc['name'] == field.data for doc in documents):
            raise validators.ValidationError('El nombre del documento ya existe para esta persona.')

        
    def validate_document_path(self, field):
        """Valida que la URL del documento sea única"""
        id = request.view_args.get('id')
        if id is None:
            raise validators.ValidationError('ID de la persona no encontrado en la URL.')
        
        documents = people.list_documents(id)
        if any(doc['url'] == field.data for doc in documents):
            raise validators.ValidationError('La URL del documento ya existe para esta persona.')
