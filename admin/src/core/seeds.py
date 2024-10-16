from datetime import datetime

from src.core import (
    adressing,
    disabilities,
    equestrian,
    people,
    professions,
    registro_pagos,
)
from src.core.user_role_permission.operations import permission_operations as Permission
from src.core.user_role_permission.operations import role_operations as Role
from src.core.user_role_permission.operations import user_operations as User


def run():

    # Seed de Permisos modulo Usuarios

    user_index = Permission.permiso_new(name='user_index')
    user_new = Permission.permiso_new(name='user_new')
    user_destroy = Permission.permiso_new(name='user_destroy')
    user_update = Permission.permiso_new(name='user_update')
    user_show = Permission.permiso_new(name='user_show')

    user_block = Permission.permiso_new(name='user_block')
    user_update_password = Permission.permiso_new(name='user_update_password')

    # Seed de Permisos modulo Equipo

    team_index = Permission.permiso_new(name='team_index')
    team_new = Permission.permiso_new(name='team_new')
    team_destroy = Permission.permiso_new(name='team_destroy')
    team_update = Permission.permiso_new(name='team_update')
    team_show = Permission.permiso_new(name='team_show')

    # Seed de Permisos modulo Registro Pagos 

    reg_pagos_index = Permission.permiso_new(name='reg_pagos_index')
    reg_pagos_new = Permission.permiso_new(name='reg_pagos_new')
    reg_pagos_destroy = Permission.permiso_new(name='reg_pagos_destroy')
    reg_pagos_update = Permission.permiso_new(name='reg_pagos_update')
    reg_pagos_show = Permission.permiso_new(name='reg_pagos_show')

    # Seed para Permisos modulo Encuestre

    encuestre_index = Permission.permiso_new(name='encuestre_index')
    encuestre_new = Permission.permiso_new(name='encuestre_new')
    encuestre_destroy = Permission.permiso_new(name='encuestre_destroy')
    encuestre_update = Permission.permiso_new(name='encuestre_update')
    encuestre_show = Permission.permiso_new(name='encuestre_show')


    # Seed para Permisos modulo Jinetes y Amazonas
    jya_index = Permission.permiso_new(name='jya_index')
    jya_new = Permission.permiso_new(name='jya_new')
    jya_destroy = Permission.permiso_new(name='jya_destroy')
    jya_update = Permission.permiso_new(name='jya_update')
    jya_show = Permission.permiso_new(name='jya_show')

    # Seed para Permisos modulo Registro Cobros
    # ...

    # Seed de Roles
    
    rol1 = Role.role_new(
        name='Tecnica',
        permissions=[encuestre_index, encuestre_show, jya_index, jya_show, jya_update, jya_new, jya_destroy]
    )
    rol2 = Role.role_new(
        name='Encuestre',
        permissions=[encuestre_index, encuestre_show, encuestre_update, encuestre_new, encuestre_destroy, jya_index, jya_show]
    )
    rol3 = Role.role_new(
        name='Voluntariado',
    )
    rol4 = Role.role_new(
        name='Administracion',
        permissions=[team_index, team_show, team_update, team_new, team_destroy,
                     reg_pagos_index, reg_pagos_show, reg_pagos_update, reg_pagos_new, reg_pagos_destroy,
                     encuestre_index, encuestre_show,
                     jya_index, jya_show, jya_update, jya_new, jya_destroy]
    )
    rol5 = Role.role_new(
        name='SystemAdmin',
        permissions=[user_index, user_new, user_destroy, user_update, user_show, user_block, user_update_password,
                     team_index, team_new, team_destroy, team_update, team_show,
                     reg_pagos_index, reg_pagos_new, reg_pagos_destroy, reg_pagos_update, reg_pagos_show,
                     encuestre_index, encuestre_new, encuestre_destroy, encuestre_update, encuestre_show,
                     jya_index, jya_new, jya_destroy, jya_update, jya_show]
    )


    # Seed de Usuarios

    user_admin = User.user_new(
        email="admin@admin.com",
        alias = "admin",
        password= "admin",
        isActive=True,
        roles=[rol5]
    )
    user1 = User.user_new(
        email="giuliana@gmail.com",
        alias = "giu",
        password="123",
        isActive=True,
        roles=[rol4,rol5]
    )
    user2 = User.user_new(
        email="lau@gmail.com",
        alias = "lau",
        password="123",
        isActive=True,
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
        tipo_pago = tipo1,
        fecha_pago= datetime.now(),
        descripcion = "h"
    )
    profession1 = professions.profession_new(
        name="Docente",
        description="Enseñanza"
    )
    job1 = professions.job_new(
        name="Docente de capacitación",
        description="Enseñanza para nuevos miembros"
    )
    job2 = professions.job_new(
        name="Administrativo/a",
        description="Gestiona tareas administrativas en oficinas, asegurando la eficiencia operativa diaria."
    )
    job3 = professions.job_new(
        name="Terapeuta",
        description="Facilita procesos de sanación y desarrollo personal mediante técnicas terapéuticas."
    )
    job4 = professions.job_new(
        name="Conductor",
        description="Monta caballos y se encarga de su manejo durante el transporte y las actividades diarias."
    )
    job5 = professions.job_new(
        name="Auxiliar de pista",
        description="Asiste en la gestión y cuidado de caballos en pistas de equitación, garantizando seguridad."
    )
    job6 = professions.job_new(
        name="Herrero",
        description="Artesano que forja metales, creando herramientas y piezas personalizadas a medida."
    )
    job7 = professions.job_new(
        name="Veterinario",
        description="Diagnostica y trata enfermedades en animales, ofreciendo cuidados preventivos y educativos."
    )
    job8 = professions.job_new(
        name="Entrenador de Caballos",
        description="Forma y entrena caballos para competencias o trabajo, desarrollando habilidades específicas."
    )
    job9 = professions.job_new(
        name="Domador",
        description="Adiestra caballos para establecer confianza y control entre el animal y el jinete."
    )
    job10 = professions.job_new(
        name="Profesor de Equitación",
        description="Enseña técnicas de monta y manejo de caballos, promoviendo seguridad en la práctica."
    )
    job11 = professions.job_new(
        name="Auxiliar de mantenimiento",
        description="Realiza mantenimiento preventivo y correctivo en instalaciones para asegurar su óptimo funcionamiento."
    )
    province1 = adressing.province_new(
        name="Buenos Aires"
    )   
    locality1 = adressing.locality_new(
        name = "Ensenada",
        province = province1
    )
    horse_document_type1 = equestrian.horse_document_type_new(
        name="Ficha general"
    )
    horse_document_type2 = equestrian.horse_document_type_new(
        name="Planificación de Entrenamiento"
    )
    horse_document_type3 = equestrian.horse_document_type_new(
        name="Informe de Evolución"
    )
    horse_document_type4 = equestrian.horse_document_type_new(
        name="Imágenes"
    )
    horse_document_type5 = equestrian.horse_document_type_new(
        name="Registro veterinario"
    )
    member1 = people.member_new(
            name="Giuliana",
            last_name="Rossi",
            dni="12345678",
            phone="123456789",
            emergency_phone=987654321,
            street="Calle Falsa",
            number=123,
            locality_id=1,
            email="giuliana@gmail.com",
            start_date="2023-01-01",
            end_date="2023-12-31",
            health_insurance="Health Inc",
            health_insurance_number=987654321,
            condition="Voluntario",
            active=True,
            profession_id=1,
            job_id=1
    )
    activity1 = equestrian.activity_new(
        name="Hipoterapia"
    )
    activity2 = equestrian.activity_new(
        name="Monta Terapéutica"
    )
    activity3 = equestrian.activity_new(
        name="Deporte Ecuestre Adaptado"
    )
    activity4 = equestrian.activity_new(
        name="Actividades Recreativas"
    )
    activity5 = equestrian.activity_new(
        name="Equitación"
    )
    horse1 = equestrian.horse_new(
        name="Canelo",
        birth_date="2001-05-04",
        gender="Macho",
        race="Criollo",
        coat="Marrón",
        donation=False,
        entry_date="2023-01-01",
        assigned_members=[member1],
        activities=[activity1, activity2, activity3],
        assigned_location="Sede principal"
    )
    horse2 = equestrian.horse_new(
        name="Summer",
        birth_date="2012-06-10",
        gender="Macho",
        race="Norteño",
        coat="Gris plateado",
        donation=True,
        entry_date="2024-03-12",
        assigned_members=[member1],
        activities=[activity3, activity2],
        assigned_location="Sede Winterfell"
    )
    disability_type1 = disabilities.disability_type_new(
        name="Mental"
    )
    disability1 = disabilities.disability_diagnosis_new(
        name="Autismo",
        type_id=disability_type1.id
    )
    parent1 = people.tutor_new_seed(
        relationship="Padre",
        name="Juan",
        last_name="Perez",
        dni="12345678",
        address="Calle Falsa 123",
        phone="123456789",
        email="juanperez@gmail.com",
        education_level="Primario",
        job="Docente"
    )
    parent2 = people.tutor_new_seed(
        relationship="Madre",
        name="Maria",
        last_name="Gomez",
        dni="22345678",
        address="Calle Verdadera 456",
        phone="223456789",
        email="mariagomez@gmail.com",
        education_level="Secundario",
        job="Enfermera"
    )
    # Creo 30 miembros para poder probar la paginación del index
    for i in range(30):
        job_id = i % 10 + 1
        member = people.member_new(
            name=f"Giuliana_{i}",
            last_name="Rossi",
            dni=f"{12345678 + i}",
            phone=f"123456789{i}",
            emergency_phone=f"987654321{i}",
            street="Calle Falsa",
            number=f"{123 + i}",
            locality=locality1,
            email=f"giuliana_{i}@gmail.com",
            start_date="2023-01-01",
            end_date="2023-12-31",
            health_insurance="Health Inc",
            health_insurance_number=f"987654321{i}",
            condition="Voluntario",
            active=True,
            profession_id=1,
            job_id=job_id
        )
        jya = people.rider_new_seed(
            name=f"Fernando_{i}",
            last_name="Alonso",
            dni=f"{22345678 + i}",
            phone=f"223456789{i}",
            emergency_phone=f"287654321{i}",
            street="Calle Verdadera",
            number=f"{223 + i}",
            health_insurance="Health Inc",
            health_insurance_number=f"287654321{i}",
            locality_id=locality1.id,
            birth_date="2002-01-01",
            grant_percentage=20,
            disability_id=disability1.id,
            family_allowance="Asignación universal por hijo",
            pension_benefit="Nacional",
            has_guardianship=True,
            city_of_birth=locality1,
            tutor_1_id=parent1.id,
            tutor_2_id=parent2.id,
            members=[member, member1]
        )
        school = people.school_new_seed(
            name=f"Escuela_{i}",
            address=f"Calle Falsa 12{i}",
            phone=f"12345678{i}",
            level="Primario",
            year=5,
            observations=f"Observaciones de la escuela {i}",
            rider_id=jya.id
        )
        job_proposal = people.job_proposal_new_seed(
            institutional_work_proposal="Hipoterapia",
            condition="Regular",
            headquarters="CASJ",
            days=["Lunes", "Miércoles", "Viernes"],
            rider_id=jya.id,
            professor_id=member.id,
            member_horse_rider_id=member.id,
            horse_id=horse1.id,
            assistant_id=member.id
        )
