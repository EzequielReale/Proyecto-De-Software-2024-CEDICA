from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import Optional, Email, EqualTo, DataRequired, Length

class UpdateForm(FlaskForm):
    """ Clase para validar formulario de actualización de un usuario."""

    alias = StringField('Alias', validators=[Optional(),
                                             Length(max=50, message="El texto no puede superar los 50 caracteres.")], default='')

    email = StringField('Email', validators=[Optional(), Email(message="Ingrese un correo electrónico válido."), 
                                             Length(max=50, message="El texto no puede superar los 50 caracteres.")], default='')
    
    roles_to_delete = SelectMultipleField('Roles para eliminar', choices=[], validators=[Optional()] , default=[])
    
    roles_to_add = SelectMultipleField('Roles para agregar', choices=[], validators=[Optional()] , default=[])

    submit = SubmitField('Confirmar cambios')


class UpdatePassword(FlaskForm):
    """ Clase para validar formulario de actualización de contraseña de un usuario."""

    password = PasswordField('Password', validators=[DataRequired(), 
                                                    Length(max=50, message="El texto no puede superar los 50 caracteres.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
                                                                     Length(max=50, message="El texto no puede superar los 50 caracteres."),
                                                                     EqualTo('password', message="Las contraseñas no coinciden.")])
    submit = SubmitField('Actualizar contraseña')

