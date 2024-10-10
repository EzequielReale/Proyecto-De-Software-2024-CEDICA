from wtforms import BooleanField, DateField, Form, SelectField, StringField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp

from src.core import people

class RiderForm(Form):
    pass