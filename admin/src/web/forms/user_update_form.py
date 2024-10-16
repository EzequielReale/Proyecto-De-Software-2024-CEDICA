from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import Optional, Email, EqualTo, DataRequired

class UpdateForm(FlaskForm):
    """ Clase para validar formulario de actualización de un usuario."""

    alias = StringField('Alias', validators=[Optional()], default='')

    email = StringField('Email', validators=[Optional(), Email(message="Ingrese un correo electrónico válido.")], default='')
    
    roles_to_delete = SelectMultipleField('Roles para eliminar', choices=[], validators=[Optional()] , default=[])
    
    roles_to_add = SelectMultipleField('Roles para agregar', choices=[], validators=[Optional()] , default=[])

    submit = SubmitField('Confirmar cambios')


class UpdatePassword(FlaskForm):
    """ Clase para validar formulario de actualización de contraseña de un usuario."""

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
                                                                     EqualTo('password', message="Las contraseñas no coinciden.")])
    submit = SubmitField('Actualizar contraseña')

