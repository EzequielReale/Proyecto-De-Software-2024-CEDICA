from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Optional, Email, EqualTo

class UpdateForm(FlaskForm):
    """ Clase para validar formulario de actualización de un usuario."""

    alias = StringField('Alias', validators=[Optional()], default='')
    email = StringField('Email', validators=[Optional(), Email()], default='')
    password = PasswordField('Password', validators=[Optional()], default='')
    confirm_password = PasswordField('Confirm Password', validators=[Optional(), EqualTo('password')], default='')
    is_active = SelectField('Estado', choices=[
        ('', 'Sin cambios'),
        ('False', 'Inactivo'),
        ('True', 'Activo'), ], validators=[Optional()], default='Sin cambios')
    role = SelectField('Rol', choices=[
            ('', 'Sin cambios'),
            ('Tecnica', 'Técnica'),
            ('Ecuestre', 'Ecuestre'),
            ('Voluntariado', 'Voluntariado'),
            ('Administracion', 'Administración')
        ], validators=[Optional()], default='Sin cambios')
    submit = SubmitField('Update')