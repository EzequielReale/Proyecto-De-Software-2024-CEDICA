from src.core import board, auth, people, professions, adressing,registro_pagos


def run():
    """Llena la base de datos con issues de prueba"""
    issue1 = board.create_issue(
        email="giu@gmail.com"
    )
    issue2= board.create_issue(
        email="yo@gmail.com"
    )
    role = auth.role_new(
        name="Administracion"
    )
    user1 = auth.user_new(
        email="giuliana@gmail.com",
        password="123",
        role = role,
        alias= "chu"
    )
    tipo1= registro_pagos.tipo_new(
        tipo="Honorarios"
    )
    tipo2= registro_pagos.tipo_new(
        tipo="Proveedor"
    ) 
    tipo3= registro_pagos.tipo_new(
        tipo="Varios"
    )
    pago = registro_pagos.pago_create(
        monto = 2000,
        beneficiario = user1,
        tipo_pago = tipo1
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
    # Creo 30 miembros para poder probar la paginación del index
    for i in range(30):
        people.member_new(
            name=f"Giuliana_{i}",
            last_name="Rossi",
            dni=f"{12345678 + i}",
            phone=f"123456789{i}",
            emergency_phone=f"987654321{i}",
            street="Calle Falsa",
            number=f"{123 + i}",
            locality_id=1,
            email=f"giuliana_{i}@gmail.com",
            start_date="2023-01-01",
            end_date="2023-12-31",
            health_insurance="Health Inc",
            health_insurance_number=f"987654321{i}",
            condition="Voluntario",
            active=True,
            profession_id=1,
            job_id=1
        )

