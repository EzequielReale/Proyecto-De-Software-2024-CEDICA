from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import Optional, ValidationError, NumberRange, Length

class UpdateJyaAParmentForm(FlaskForm):

    # Validador personalizado para asegurarse de que el valor sea positivo
    def positive_check(form, field):
        if field.data is None or field.data <= 0:
            raise ValidationError('El valor debe ser un número positivo.')
        
    jinete_amazona = SelectField('Jinete o Amazona', choices=[] ,validators=[Optional()])
    fecha_pago = DateField('Fecha de pago', format='%Y-%m-%d', validators=[Optional()])
    medio_de_pago = SelectField('Medio de pago', choices=[], validators=[Optional()])
    monto = FloatField('Monto', validators=[Optional(), positive_check,
                                            NumberRange(min=0, max=9999999, message="El valor debe estar entre 0 y 9999999.")])
    receptor = SelectField('Receptor', choices=[], validators=[Optional()])
    estado_de_pago = SelectField('Estado de pago', choices=[('1', 'En deuda'), ('0', 'Pagado')], validators=[Optional()])
    observaciones = StringField('Observaciones', validators=[Optional(),
                                                             Length(max=99, message="El texto no puede superar los 99 caracteres.")])
    submit = SubmitField('Actualizar cobro')

    