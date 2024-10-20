from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Optional

estados_choices = [('', 'Selecciona una opción'),('1', 'En deuda'), ('0', 'Pagado') ]


class RegisterJyAPaymentForm(FlaskForm):
    """ Clase para validar formulario de registro de nuevo cobro."""

    jya = SelectField('Jinete o Amazona', choices=[] ,validators=[DataRequired()])
    fecha_pago = DateField('Fecha de pago', format='%Y-%m-%d', validators=[DataRequired()])
    medio_de_pago = SelectField('Medio de pago', choices=[], validators=[DataRequired()])
    monto_pago = FloatField('Monto', validators=[DataRequired()])
    receptor = SelectField('Receptor', choices=[], validators=[DataRequired()])
    estado_de_pago = SelectField('Estado de pago', choices=estados_choices, validators=[DataRequired()])
    observaciones = StringField('Observaciones', validators=[Optional()])
    submit = SubmitField('Registrar cobro')


