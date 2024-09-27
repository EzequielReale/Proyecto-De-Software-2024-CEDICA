from src.core import board, auth, people, professions, adressing


def run():
    """Llena la base de datos con issues de prueba"""
    issue1 = board.create_issue(
        email="giu@gmail.com"
    )
    issue2= board.create_issue(
        email="yo@gmail.com"
    )
    user1 = auth.user_new(
        email="giuliana@gmail.com",
        password="123"
    )
    profession1 = professions.profession_new(
        name="Docente",
        description="Enseñanza"
    )
    job1 = professions.job_new(
        name="Docente de capacitación",
        description="Enseñanza para nuevos miembros"
    )
    province1 = adressing.province_new(
        name="Buenos Aires"
    )
    locality1 = adressing.locality_new(
        name="Berisso",
        postal_code="1923",
        province_id=1
    )
    member1 = people.member_new(
            name="Giuliana",
            last_name="Rossi",
            dni="12345678",
            phone="123456789",
            emergency_phone="987654321",
            street="Calle Falsa",
            number="123",
            locality_id=1,
            email="giuliana@gmail.com",
            start_date="2023-01-01",
            end_date="2023-12-31",
            health_insurance="Health Inc.",
            health_insurance_number="987654321",
            condition="Voluntario",
            active=True,
            profession_id=1,
            job_id=1
    )

