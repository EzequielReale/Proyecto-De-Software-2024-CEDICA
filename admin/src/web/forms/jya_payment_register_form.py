from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Optional, ValidationError, NumberRange, Length

estados_choices = [('', 'Selecciona una opción'),('1', 'En deuda'), ('0', 'Pagado') ]


class RegisterJyAPaymentForm(FlaskForm):
    """ Clase para validar formulario de registro de nuevo cobro."""


    # Validador personalizado para asegurarse de que el valor sea positivo
    def positive_check(form, field):
        if field.data is None or field.data <= 0:
            raise ValidationError('El valor debe ser un número positivo.')
        
    jya = SelectField('Jinete o Amazona', choices=[] ,validators=[DataRequired()])
    fecha_pago = DateField('Fecha de pago', format='%Y-%m-%d', validators=[DataRequired()])
    medio_de_pago = SelectField('Medio de pago', choices=[], validators=[DataRequired()])
    monto_pago = FloatField('Monto', validators=[DataRequired() , positive_check,
                                                 NumberRange(min=0, max=9999999, message="El valor debe estar entre 0 y 9999999.")])
    receptor = SelectField('Receptor', choices=[], validators=[DataRequired()])
    estado_de_pago = SelectField('Estado de pago', choices=estados_choices, validators=[DataRequired()])
    observaciones = StringField('Observaciones', validators=[Optional(),
                                                             Length(max=99, message="El texto no puede superar los 99 caracteres.")])
    submit = SubmitField('Registrar cobro')


    