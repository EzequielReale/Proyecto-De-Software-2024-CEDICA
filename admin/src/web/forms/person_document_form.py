from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms import SelectField
from wtforms.validators import Optional


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
