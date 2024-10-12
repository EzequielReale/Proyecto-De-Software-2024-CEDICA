from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SelectField, SubmitField, validators
from wtforms.validators import Optional

from src.core import people


class PersonDocumentForm(FlaskForm):
    document = FileField('Subir archivo', validators=[
        FileRequired(message='No se ha seleccionado ningún archivo.'),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx'], 'Tipos de archivo permitidos: pdf, png, jpg, jpeg, doc, docx, xls, xlsx.')
    ])
    document_type = SelectField('Tipo de documento', choices=[
        ('Entrevista', 'Entrevista'),
        ('Evaluación', 'Evaluación'),
        ('Planificaciones', 'Planificaciones'),
        ('Evolución', 'Evolución'),
        ('Crónicas', 'Crónicas'),
        ('Documental', 'Documental')
    ], validators=[Optional()])
    submit = SubmitField('Guardar')

    def validate_document(self, field) -> None:
        """Valida que el nombre del documento sea único"""
        id = request.view_args.get('id')
        if id is None:
            raise validators.ValidationError('ID de la persona no encontrado en la URL.')
        
        documents = people.list_documents(id)
        if any(doc['name'] == field.data.filename for doc in documents):
            raise validators.ValidationError('El nombre del documento ya existe para esta persona.')