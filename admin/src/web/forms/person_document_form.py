from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class PersonDocumentForm(FlaskForm):
    document = FileField('Subir archivo', validators=[
        FileRequired(message='No se ha seleccionado ningún archivo.'),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'], 'Tipos de archivo permitidos: pdf, png, jpg, jpeg, doc, docx.')
    ])
    submit = SubmitField('Guardar')
