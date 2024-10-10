from src.core.user_role_permission.operations import role_operations as Role
from src.core.user_role_permission.operations import user_operations as User
from src.core.user_role_permission.operations import role_operations as Role
from src.core.user_role_permission.operations import permission_operations as Permission
from datetime import datetime
from src.core import disabilities, people, professions, adressing, registro_pagos, equestrian


def run():

    # Seed de Permisos modulo Usuarios

    user_index = Permission.permiso_new(name='user_index')
    user_new = Permission.permiso_new(name='user_new')
    user_destroy = Permission.permiso_new(name='user_destroy')
    user_update = Permission.permiso_new(name='user_update')
    user_show = Permission.permiso_new(name='user_show')

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
    # ...

    # Seed para Permisos modulo Registro Cobros
    # ...

    # Seed de Roles

    rol1 = Role.role_new(
        name='Tecnica',
        permissions=[encuestre_index, encuestre_show]
    )
    rol2 = Role.role_new(
        name='Encuestre',
        permissions=[encuestre_index, encuestre_show, encuestre_update, encuestre_new, encuestre_destroy]
    )
    rol3 = Role.role_new(
        name='Voluntariado',
    )
    rol4 = Role.role_new(
        name='Administracion',
        permissions=[team_index, team_show, team_update, team_new, team_destroy,
                     reg_pagos_index, reg_pagos_show, reg_pagos_update, reg_pagos_new, reg_pagos_destroy,
                     encuestre_index, encuestre_show]
    )
    rol5 = Role.role_new(
        name='SystemAdmin',
        permissions=[user_index, user_new, user_destroy, user_update, user_show]
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
    )
    user2 = User.user_new(
        email="lau@gmail.com",
        alias = "lau",
        password="123",
        isActive=True,
    )
    # permiso = auth.permiso_new(
    #    name="administracion_index"
    # )
    # permiso2 = auth.permiso_new(
    #    name="administracion_show"
    # )
    # role = auth.role_new(
    #   name="Administracion",
    #   permissions = [permiso,permiso2]
    # )
    # user1 = auth.user_new(
    #     email="giuliana@gmail.com",
    #     password="123",
    #     roles=[role],
    #     alias="chu"
    # )
    # user2 = auth.user_new(
    #     email="chu@gmail.com",
    #     password="123",
    #     alias="chu"
    # )
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
    province1 = adressing.province_new(
        name="Buenos Aires"
    )   
    locality1 = adressing.locality_new(
        name = "Ensenada",
        province = province1
    )
    member1 = people.member_new(
            name="Giuliana",
            last_name="Rossi",
            dni="12345678",
            phone="123456789",
            emergency_phone=987654321,
            street="Calle Falsa",
            number=123,
            locality=locality1,
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
    disability_type1 = disabilities.disability_type_new(
        name="Mental"
    )
    disability1 = disabilities.disability_diagnosis_new(
        name="Autismo",
        type_id=disability_type1.id  # Ensure the ID is used
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
            locality=locality1,
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
        people.rider_new(
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
            city_of_birth=locality1
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
