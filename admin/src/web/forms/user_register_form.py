from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    """ Clase para validar formulario de registro de un usuario."""

    alias = StringField('Alias', validators=[DataRequired(),
                                             Length(max=50, message="El texto no puede superar los 50 caracteres.")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Ingrese un correo electrónico válido."),
                                             Length(max=50, message="El texto no puede superar los 50 caracteres.")])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(max=50, message="El texto no puede superar los 50 caracteres.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
                                                                    EqualTo('password' , message="Las contraseñas no coinciden."),
                                                                    Length(max=50, message="El texto no puede superar los 50 caracteres.")])
    role = SelectMultipleField('Rol', choices=[
        ('Tecnica', 'Técnica'),
        ('Encuestre', 'Ecuestre'),
        ('Voluntariado', 'Voluntariado'),
        ('Administracion', 'Administración')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrar')