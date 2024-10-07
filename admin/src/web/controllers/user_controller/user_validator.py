from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    """ Clase para validar formulario de registro de un usuario."""

    alias = StringField('Alias', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[
        ('Tecnica', 'Técnica'),
        ('Encuestre', 'Ecuestre'),
        ('Voluntariado', 'Voluntariado'),
        ('Administracion', 'Administración')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrar')

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


class SearchForm(FlaskForm):
    """ Clase para formulario de búsqueda de un usuario."""
    email = StringField('Email', validators=[Optional()], default='',
                                 render_kw={"placeholder": "Escriba un email...", 
                                "style": "width: 30%; padding: 5px; border: 2px solid #ccc; border-radius: 25px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);"})

    status = SelectField('Estado', choices=[
                        ('', 'Todos'), 
                        ('True', 'Activo'), 
                        ('False', 'Inactivo')], 
                         validators=[Optional()] , default='Todos')
    
    role = SelectField('Rol', choices=[
                        ('', 'Todos'),
                        ('Tecnica', 'Técnica'),
                        ('Ecuestre', 'Ecuestre'),
                        ('Voluntariado', 'Voluntariado'),
                        ('Administracion', 'Administración')], 
                         validators=[Optional()] , default='Todos')
                              
    submit = SubmitField('Buscar')