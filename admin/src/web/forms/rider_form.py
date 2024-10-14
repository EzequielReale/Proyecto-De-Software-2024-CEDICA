from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    SelectField,
    SelectMultipleField,
    StringField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    Optional,
    Regexp,
    ValidationError,
)

from src.core import people


class RiderForm(FlaskForm):
    """Formulario para la creación y edición de jinetes/amazonas"""
    
    def __init__(self, *args, **kwargs):
        """Inicializa el formulario"""
        self.rider_id = kwargs.pop('rider_id', None)
        super(RiderForm, self).__init__(*args, **kwargs)


    name = StringField(
        "Nombre",
        [
            DataRequired(),
            Regexp(
                r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$",
                message="Nombre solo puede contener letras",
            ),
            Length(max=64),
        ],
    )
    last_name = StringField(
        "Apellido",
        [
            DataRequired(),
            Regexp(
                r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$",
                message="Apellido solo puede contener letras",
            ),
            Length(max=64),
        ],
    )
    dni = StringField(
        "DNI",
        [
            DataRequired(),
            Regexp(r"^[0-9]+$", message="DNI debe contener solo números"),
            Length(max=9),
        ],
    )
    phone = StringField(
        "Teléfono",
        [
            DataRequired(),
            Regexp(r"^[0-9\s-]+$", message="Teléfono no puede tener letras"),
            Length(max=15),
        ],
    )
    emergency_phone = StringField(
        "Teléfono de emergencia",
        [
            DataRequired(),
            Regexp(
                r"^[0-9\s-]+$", message="Teléfono de emergencia no puede tener letras"
            ),
            Length(max=15),
        ],
    )
    birth_date = DateField("Fecha de nacimiento", [DataRequired()])
    province_of_birth = SelectField("Provincia de nacimiento", [DataRequired()], choices=[], coerce=int)
    city_of_birth = SelectField("Localidad de nacimiento", [DataRequired()], choices=[], coerce=int)
    has_disability_certificate = SelectField(
        "¿Tiene certificado de discapacidad?",
        [DataRequired()],
        choices=[("True", "Sí"), ("False", "No")],
    )
    disability_type = SelectField("Tipo de discapacidad", [Optional()], choices=[])
    disability_id = SelectField("Diagnóstico de discapacidad", [Optional()], choices=[])
    health_insurance = StringField("Obra social", [DataRequired(), Length(max=32)])
    health_insurance_number = StringField(
        "Número de obra social",
        [
            DataRequired(),
            Regexp(
                r"^[0-9]+$", message="Número de obra social debe contener solo números"
            ),
            Length(max=32),
        ],
    )
    province_id = SelectField("Provincia de domicilio", [DataRequired()], choices=[], coerce=int)
    locality_id = SelectField("Localidad de domicilio", [DataRequired()], choices=[], coerce=int)
    street = StringField("Calle", [DataRequired(), Length(max=64)])
    number = StringField(
        "Número",
        [
            DataRequired(),
            Regexp(r"^[0-9]+$", message="Número debe contener solo números"),
            Length(max=8),
        ],
    )
    floor = StringField(
        "Piso",
        [
            Optional(),
            Regexp(r"^[0-9]+$", message="Piso debe contener solo números"),
            Length(max=4),
        ],
    )
    apartment = StringField("Departamento", [Optional(), Length(max=8)])
    has_family_allowance = SelectField(
        "¿Recibe asignación familiar?",
        [DataRequired()],
        choices=[("True", "Sí"), ("False", "No")],
    )
    family_allowance = SelectField(
        "Asignación familiar",
        [Optional()],
        choices=[
            ("Asignación universal por hijo", "Asignación universal por hijo"),
            (
                "Asignación universal por hijo con discapacidad",
                "Asignación universal por hijo con discapacidad",
            ),
            (
                "Asignación por ayuda escolar anual",
                "Asignación por ayuda escolar anual",
            ),
        ],
    )
    has_pension = SelectField(
        "¿Recibe pensión?", [DataRequired()], choices=[("True", "Sí"), ("False", "No")]
    )
    pension_benefit = SelectField(
        "Tipo de pensión",
        [Optional()],
        choices=[("Nacional", "Nacional"), ("Provincial", "Provincial")],
    )
    has_grant = SelectField(
        "¿Está becado?", [DataRequired()], choices=[("True", "Sí"), ("False", "No")]
    )
    grant_percentage = StringField(
        "Porcentaje de beca",
        [
            Optional(),
            Regexp(
                r"^[0-9]+(\.[0-9]{1,2})?$",
                message="Porcentaje debe ser un número válido",
            ),
        ],
    )
    has_guardianship = SelectField(
        "¿Tiene tutela legal?",
        [DataRequired()],
        choices=[("True", "Sí"), ("False", "No")],
    )

    has_tutor_1 = SelectField(
        "¿Tiene tutor?", [DataRequired()], choices=[("True", "Sí"), ("False", "No")]
    )
    tutor1_relationship = SelectField(
        "Relación",
        [Optional()],
        choices=[("Padre", "Padre"), ("Madre", "Madre"), ("Tutor", "Tutor")],
    )
    tutor1_dni = StringField(
        "DNI",
        [
            Optional(),
            Regexp(r"^[0-9]+$", message="DNI debe contener solo números"),
            Length(max=9),
        ],
    )
    tutor1_name = StringField("Nombre", [Optional(), Length(max=64)])
    tutor1_last_name = StringField("Apellido", [Optional(), Length(max=64)])
    tutor1_phone = StringField(
        "Teléfono",
        [
            Optional(),
            Regexp(r"^[0-9\s-]+$", message="Teléfono no puede tener letras"),
            Length(max=32),
        ],
    )
    tutor1_email = StringField("Email", [Optional(), Email(), Length(max=64)])
    tutor1_address = StringField("Dirección", [Optional(), Length(max=128)])
    tutor1_education_level = SelectField(
        "Nivel educativo",
        [Optional()],
        choices=[
            ("Primario", "Primario"),
            ("Secundario", "Secundario"),
            ("Terciario", "Terciario"),
            ("Universitario", "Universitario"),
        ],
    )
    tutor1_job = StringField("Trabajo", [Optional(), Length(max=64)])

    has_tutor_2 = SelectField(
        "¿Tiene otro tutor?", [Optional()], choices=[("True", "Sí"), ("False", "No")]
    )
    tutor2_relationship = SelectField(
        "Relación",
        [Optional()],
        choices=[("Padre", "Padre"), ("Madre", "Madre"), ("Tutor", "Tutor")],
    )
    tutor2_dni = StringField(
        "DNI",
        [
            Optional(),
            Regexp(r"^[0-9]+$", message="DNI debe contener solo números"),
            Length(max=9),
        ],
    )
    tutor2_name = StringField("Nombre", [Optional(), Length(max=64)])
    tutor2_last_name = StringField("Apellido", [Optional(), Length(max=64)])
    tutor2_phone = StringField(
        "Teléfono",
        [
            Optional(),
            Regexp(r"^[0-9\s-]+$", message="Teléfono no puede tener letras"),
            Length(max=32),
        ],
    )
    tutor2_email = StringField("Email", [Optional(), Email(), Length(max=64)])
    tutor2_address = StringField("Dirección", [Optional(), Length(max=128)])
    tutor2_education_level = SelectField(
        "Nivel educativo",
        [Optional()],
        choices=[
            ("Primario", "Primario"),
            ("Secundario", "Secundario"),
            ("Terciario", "Terciario"),
            ("Universitario", "Universitario"),
        ],
    )
    tutor2_job = StringField("Trabajo", [Optional(), Length(max=64)])

    assigned_professionals = SelectMultipleField(
        "Profesionales", [Optional()], choices=[], coerce=int
    )

    has_school = SelectField(
        "¿Asiste a la escuela?",
        [DataRequired()],
        choices=[("True", "Sí"), ("False", "No")],
    )
    school_name = StringField("Nombre de la escuela", [Optional(), Length(max=64)])
    school_address = StringField(
        "Dirección de la escuela", [Optional(), Length(max=128)]
    )
    school_phone = StringField(
        "Teléfono de la escuela",
        [
            Optional(),
            Regexp(
                r"^[0-9\s-]+$", message="Teléfono de la escuela no puede tener letras"
            ),
            Length(max=16),
        ],
    )
    school_level = SelectField(
        "Nivel educativo",
        [Optional()],
        choices=[
            ("Inicial", "Inicial"),
            ("Primario", "Primario"),
            ("Secundario", "Secundario"),
            ("Terciario", "Terciario"),
            ("Universitario", "Universitario"),
        ],
    )
    school_year = IntegerField(
        "Año",
        [
            Optional(),
            NumberRange(min=1, max=12, message="Año debe ser un número entre 1 y 12"),
        ],
    )
    school_observations = StringField("Observaciones", [Optional()])

    has_job_proposal = SelectField(
        "¿Tiene una oferta de trabajo con nosotros?",
        [DataRequired()],
        choices=[("True", "Sí"), ("False", "No")],
    )
    institutional_work_proposal = SelectField(
        "Propuesta de trabajo institucional",
        [Optional()],
        choices=[
            ("Hipoterapia", "Hipoterapia"),
            ("Monta Terapéutica", "Monta Terapéutica"),
            ("Deporte Ecuestre Adaptado", "Deporte Ecuestre Adaptado"),
            ("Actividades Recreativas", "Actividades Recreativas"),
            ("Equitación", "Equitación"),
        ],
    )
    condition = SelectField(
        "Condición",
        [Optional()],
        choices=[("Regular", "Regular"), ("De baja", "De baja")],
    )
    headquarters = SelectField(
        "Sede",
        [Optional()],
        choices=[("CASJ", "CASJ"), ("HLP", "HLP"), ("OTRO", "OTRO")],
    )
    days = SelectMultipleField(
        "Días",
        [Optional()],
        choices=[
            ("Lunes", "Lunes"),
            ("Martes", "Martes"),
            ("Miércoles", "Miércoles"),
            ("Jueves", "Jueves"),
            ("Viernes", "Viernes"),
            ("Sábado", "Sábado"),
            ("Domingo", "Domingo"),
        ],
        coerce=int,
    )
    professor_id = SelectField("Profesor o terapeuta", [Optional()], choices=[], coerce=int)
    assistant_id = SelectField("Auxiliar de pista", [Optional()], choices=[], coerce=int)
    member_horse_rider_id = SelectField(
        "Conductor del caballo", [Optional()], choices=[], coerce=int
    )
    horse_id = SelectField("Caballo", [Optional()], choices=[], coerce=int)


    def process(self, formdata=None, obj=None, **kwargs):
        """Preprocesa los datos antes de la validación y pasa los nombres a mayúsculas"""
        super().process(formdata, obj, **kwargs)
        if self.name.data:
            self.name.data = self.name.data.title()
        if self.last_name.data:
            self.last_name.data = self.last_name.data.title()
        if self.street.data:
            self.street.data = self.street.data.title()
        if self.school_name.data:
            self.school_name.data = self.school_name.data.title()
        if self.tutor1_name.data:
            self.tutor1_name.data = self.tutor1_name.data.title()
        if self.tutor1_last_name.data:
            self.tutor1_last_name.data = self.tutor1_last_name.data.title()
        if self.tutor2_name.data:
            self.tutor2_name.data = self.tutor2_name.data.title()
        if self.tutor2_last_name.data:
            self.tutor2_last_name.data = self.tutor2_last_name
    
        # Debug statements to check values
        print(f"City of Birth: {self.city_of_birth.data}")
        print(f"Locality ID: {self.locality_id.data}")


    def validate(self, extra_validators=None):
        if not super(RiderForm, self).validate(extra_validators=extra_validators):
            return False
        if self.has_disability_certificate.data == "True":
            if not self.disability_type.data:
                self.disability_type.errors.append("Este campo es obligatorio.")
                return False
            if not self.disability_id.data:
                self.disability_id.errors.append("Este campo es obligatorio.")
                return False
        if self.has_family_allowance.data == "True":
            if not self.family_allowance.data:
                self.family_allowance.errors.append("Este campo es obligatorio.")
                return False
        if self.has_pension.data == "True":
            if not self.pension_benefit.data:
                self.pension_benefit.errors.append("Este campo es obligatorio.")
                return False
        if self.has_grant.data == "True":
            if not self.grant_percentage.data:
                self.grant_percentage.errors.append("Este campo es obligatorio.")
                return False
        if self.has_job_proposal.data == "True":
            required_fields = [
                "institutional_work_proposal",
                "condition",
                "headquarters",
                "days",
                "professor_id",
                "assistant_id",
                "member_horse_rider_id",
                "horse_id",
            ]
            for field in required_fields:
                if not getattr(self, field).data:
                    getattr(self, field).errors.append("Este campo es obligatorio.")
                    return False
        if self.has_school.data == "True":
            required_school_fields = [
                "school_name",
                "school_address",
                "school_phone",
                "school_level",
                "school_year",
            ]
            for field in required_school_fields:
                if not getattr(self, field).data:
                    getattr(self, field).errors.append("Este campo es obligatorio.")
                    return False
        if self.has_tutor_1.data == "True":
            required_tutor1_fields = [
                "tutor1_relationship",
                "tutor1_dni",
                "tutor1_name",
                "tutor1_last_name",
                "tutor1_phone",
                "tutor1_email",
                "tutor1_address",
                "tutor1_education_level",
                "tutor1_job",
            ]
            for field in required_tutor1_fields:
                if not getattr(self, field).data:
                    getattr(self, field).errors.append("Este campo es obligatorio.")
                    return False
        if self.has_tutor_2.data == "True":
            required_tutor2_fields = [
                "tutor2_relationship",
                "tutor2_dni",
                "tutor2_name",
                "tutor2_last_name",
                "tutor2_phone",
                "tutor2_email",
                "tutor2_address",
                "tutor2_education_level",
                "tutor2_job",
            ]
            for field in required_tutor2_fields:
                if not getattr(self, field).data:
                    getattr(self, field).errors.append("Este campo es obligatorio.")
                    return False
        
        return True


    def validate_dni(form, field):
        """Valida que el DNI no esté repetido"""
        if people.get_rider_by_field('dni', field.data, exclude_id=form.rider_id):
            raise ValidationError("Ya existe un jinete/amazona con ese DNI")
        

    def validate_phone(form, field):
        """Valida que el teléfono no sea igual al teléfono de emergencia"""
        if field.data == form.emergency_phone.data:
            raise ValidationError("El teléfono y el teléfono de emergencia no pueden ser el mismo")
        

    def validate_birth_date(form, field):
        """Valida que el jinete/amazona tenga al menos 3 años"""

        birth_year = field.data.year
        current_year = datetime.now().year

        if current_year - birth_year < 3:
            raise ValidationError("El jinete/amazona debe tener al menos 3 años")


    def get_rider_data(self):
        return {
            "name": self.name.data,
            "last_name": self.last_name.data,
            "dni": self.dni.data,
            "phone": self.phone.data,
            "emergency_phone": self.emergency_phone.data,
            "birth_date": self.birth_date.data,
            "city_of_birth": int(self.city_of_birth.data),
            "disability_id": int(self.disability_id.data) if self.disability_id.data else None,
            "health_insurance": self.health_insurance.data,
            "health_insurance_number": self.health_insurance_number.data,
            "locality_id": int(self.locality_id.data),
            "street": self.street.data,
            "number": self.number.data,
            "floor": self.floor.data,
            "apartment": self.apartment.data,
            "family_allowance": self.family_allowance.data,
            "pension_benefit": self.pension_benefit.data,
            "grant_percentage": float(self.grant_percentage.data) if self.grant_percentage.data else None,
            "has_guardianship": self.has_guardianship.data == "True",
        }


    def get_school_data(self):
        return {
            "name": self.school_name.data,
            "address": self.school_address.data,
            "phone": self.school_phone.data,
            "level": self.school_level.data,
            "year": self.school_year.data,
            "observations": self.school_observations.data,
        }


    def get_tutor_data(self, tutor_number):
        if tutor_number == 1:
            return {
                "relationship": self.tutor1_relationship.data,
                "dni": self.tutor1_dni.data,
                "name": self.tutor1_name.data,
                "last_name": self.tutor1_last_name.data,
                "phone": self.tutor1_phone.data,
                "email": self.tutor1_email.data,
                "address": self.tutor1_address.data,
                "education_level": self.tutor1_education_level.data,
                "job": self.tutor1_job.data,
            }
        elif tutor_number == 2:
            return {
                "relationship": self.tutor2_relationship.data,
                "dni": self.tutor2_dni.data,
                "name": self.tutor2_name.data,
                "last_name": self.tutor2_last_name.data,
                "phone": self.tutor2_phone.data,
                "email": self.tutor2_email.data,
                "address": self.tutor2_address.data,
                "education_level": self.tutor2_education_level.data,
                "job": self.tutor2_job.data,
            }


    def get_job_proposal_data(self):
        return {
            "institutional_work_proposal": self.institutional_work_proposal.data,
            "condition": self.condition.data,
            "headquarters": self.headquarters.data,
            "days": self.days.data,
            "professor_id": self.professor_id.data,
            "assistant_id": self.assistant_id.data,
            "member_horse_rider_id": self.member_horse_rider_id.data,
            "horse_id": self.horse_id.data,
        }
