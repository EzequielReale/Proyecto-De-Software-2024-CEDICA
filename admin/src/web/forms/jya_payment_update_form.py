from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import Optional

class UpdateJyaAParmentForm(FlaskForm):

    jinete_amazona = SelectField('Jinete o Amazona', choices=[] ,validators=[Optional()])
    fecha_pago = DateField('Fecha de pago', format='%Y-%m-%d', validators=[Optional()])
    medio_de_pago = SelectField('Medio de pago', choices=[], validators=[Optional()])
    monto = FloatField('Monto', validators=[Optional()])
    receptor = SelectField('Receptor', choices=[], validators=[Optional()])
    estado_de_pago = SelectField('Estado de pago', choices=[('1', 'En deuda'), ('0', 'Pagado')], validators=[Optional()])
    observaciones = StringField('Observaciones', validators=[Optional()])
    submit = SubmitField('Actualizar cobro')