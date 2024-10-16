from wtforms import (
    BooleanField,
    DateField,
    Form,
    SelectField,
    StringField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp

from src.core import people


class MemberForm(Form):
    
    def __init__(self, *args, **kwargs):
        """Inicializa el formulario"""
        self.member_id = kwargs.pop('member_id', None)
        super(MemberForm, self).__init__(*args, **kwargs)

    name = StringField('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Regexp(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El nombre no debe contener números"),
        Length(min=1, max=64)
    ])
    last_name = StringField('Apellido', validators=[
        DataRequired(message="El apellido es obligatorio"),
        Regexp(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El apellido no debe contener números"),
        Length(min=1, max=64)
    ])
    dni = StringField('DNI', validators=[
        DataRequired(message="El DNI es obligatorio"),
        Regexp(r'^\d+$', message="El DNI no debe contener letras"),
        Length(min=7, max=10)
    ])
    phone = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio"),
        Regexp(r'^[0-9+\-\s]+$', message="El teléfono solo puede contener números, espacios, + y -"),
        Length(min=7, max=32)
    ])
    emergency_phone = StringField('Teléfono de emergencia', validators=[
        DataRequired(message="El teléfono de emergencia es obligatorio"),
        Regexp(r'^[0-9+\-\s]+$', message="El teléfono de emergencia solo puede contener números, espacios, + y -"),
        Length(min=7, max=32)
    ])
    street = StringField('Calle', validators=[
        DataRequired(message="La calle es obligatoria"),
        Length(min=2, max=128)
    ])
    number = StringField('Número', validators=[
        DataRequired(message="El número es obligatorio"),
        Regexp(r'^\d+$', message="El número no debe contener letras"),
        Length(min=1, max=8)
    ])
    email = StringField('Email', validators=[
        DataRequired(message="El email es obligatorio"),
        Email(message="El email no es válido")
    ])
    start_date = DateField('Fecha de inicio', format='%Y-%m-%d', validators=[
        DataRequired(message="La fecha de inicio es obligatoria")
    ])
    end_date = DateField('Fecha de cese', format='%Y-%m-%d', validators=[
        Optional()
    ])
    health_insurance = StringField('Obra social', validators=[
        DataRequired(message="La obra social es obligatoria"),
        Regexp(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', message="El nombre de la obra social no debe contener números"),
        Length(min=1, max=32)
    ])
    health_insurance_number = StringField('Número de obra social', validators=[
        DataRequired(message="El número de la obra social es obligatorio"),
        Regexp(r'^\d+$', message="El número de la obra social no debe contener letras"),
        Length(min=1, max=32)
    ])
    condition = SelectField('Condición', choices=[
        ('Voluntario', 'Voluntario'),
        ('Personal Rentado', 'Personal Rentado')
    ], validators=[DataRequired(message="La condición es obligatoria")])
    active = BooleanField('Activo', validators=[Optional()])
    locality_id = SelectField('Localidad', coerce=int, validators=[DataRequired(message="La localidad es obligatoria")])
    profession_id = SelectField('Profesión', coerce=int, validators=[DataRequired(message="La profesión es obligatoria")])
    job_id = SelectField('Trabajo', coerce=int, validators=[DataRequired(message="El trabajo es obligatorio")])

    def process(self, formdata=None, obj=None, **kwargs):
        """Preprocesa los datos antes de la validación"""
        super().process(formdata, obj, **kwargs)
        if self.name.data:
            self.name.data = self.name.data.title()
        if self.last_name.data:
            self.last_name.data = self.last_name.data.title()

    def validate_end_date(form, field):
        """Valida que la fecha de cese sea posterior a la fecha de inicio"""
        if field.data and field.data <= form.start_date.data:
            raise ValidationError("La fecha de cese debe ser posterior a la fecha de inicio")

    def validate_dni(form, field):
        """Valida que el DNI no esté repetido"""
        if people.get_member_by_field('dni', field.data, exclude_id=form.member_id):
            raise ValidationError("Ya existe un miembro con ese DNI")
        
    def validate_email(form, field):
        """Valida que el email no esté repetido"""
        if people.get_member_by_field('email', field.data, exclude_id=form.member_id):
            raise ValidationError("Ya existe un miembro con ese email")
        
    def validate_phone(form, field):
        """Valida que el teléfono no sea igual al teléfono de emergencia"""
        if field.data == form.emergency_phone.data:
            raise ValidationError("El teléfono y el teléfono de emergencia no pueden ser el mismo")
