from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    """ Clase para validar formulario de registro de un usuario."""

    alias = StringField('Alias', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message="Ingrese un correo electrónico válido.")])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
                                                                    EqualTo('password' , message="Las contraseñas no coinciden.")])
    role = SelectMultipleField('Rol', choices=[
        ('Tecnica', 'Técnica'),
        ('Ecuestre', 'Ecuestre'),
        ('Voluntariado', 'Voluntariado'),
        ('Administracion', 'Administración')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrar')