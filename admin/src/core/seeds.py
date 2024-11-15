from datetime import datetime, timedelta
from faker import Faker
import random

from src.core import (
    adressing,
    disabilities,
    equestrian,
    people,
    professions,
    registro_pagos,
    registro_pagos_jya,
    content_admin
)
from src.core.user_role_permission.operations import permission_operations as Permission
from src.core.user_role_permission.operations import role_operations as Role
from src.core.user_role_permission.operations import user_operations as User
from src.core.content_admin.article_status_enum import ArticleStatus
from datetime import datetime



fake = Faker()

fecha_inicio = datetime(2023, 1, 1, 0, 0, 0)
fecha_fin = datetime(2024, 12, 31, 23, 59, 59)

def generar_fecha_y_hora_aleatoria(inicio: datetime, fin: datetime) -> datetime:
    """Recibe dos fechas y devuelve una fecha y hora aleatoria entre ambas."""
    # Calcular la diferencia en segundos entre las dos fechas
    diferencia_en_segundos = int((fin - inicio).total_seconds())
    # Generar un número aleatorio de segundos dentro de esa diferencia
    segundos_aleatorios = random.randrange(diferencia_en_segundos)
    # Sumar los segundos aleatorios a la fecha de inicio
    return inicio + timedelta(seconds=segundos_aleatorios)


def _seed_users():
    # Seed de Permisos modulo Usuarios
    user_index = Permission.permiso_new(name="user_index")
    user_new = Permission.permiso_new(name="user_new")
    user_destroy = Permission.permiso_new(name="user_destroy")
    user_update = Permission.permiso_new(name="user_update")
    user_show = Permission.permiso_new(name="user_show")
    user_block = Permission.permiso_new(name="user_block")
    user_update_password = Permission.permiso_new(name="user_update_password")

    # Seed de Permisos modulo Equipo
    team_index = Permission.permiso_new(name="team_index")
    team_new = Permission.permiso_new(name="team_new")
    team_destroy = Permission.permiso_new(name="team_destroy")
    team_update = Permission.permiso_new(name="team_update")
    team_show = Permission.permiso_new(name="team_show")

    # Seed de Permisos modulo Registro Pagos
    reg_pagos_index = Permission.permiso_new(name="reg_pagos_index")
    reg_pagos_new = Permission.permiso_new(name="reg_pagos_new")
    reg_pagos_destroy = Permission.permiso_new(name="reg_pagos_destroy")
    reg_pagos_update = Permission.permiso_new(name="reg_pagos_update")
    reg_pagos_show = Permission.permiso_new(name="reg_pagos_show")

    # Seed para Permisos modulo Encuestre
    encuestre_index = Permission.permiso_new(name="encuestre_index")
    encuestre_new = Permission.permiso_new(name="encuestre_new")
    encuestre_destroy = Permission.permiso_new(name="encuestre_destroy")
    encuestre_update = Permission.permiso_new(name="encuestre_update")
    encuestre_show = Permission.permiso_new(name="encuestre_show")

    # Seed para Permisos modulo Jinetes y Amazonas
    jya_index = Permission.permiso_new(name="jya_index")
    jya_new = Permission.permiso_new(name="jya_new")
    jya_destroy = Permission.permiso_new(name="jya_destroy")
    jya_update = Permission.permiso_new(name="jya_update")
    jya_show = Permission.permiso_new(name="jya_show")

    # Seed para Permisos modulo Registro Cobros
    reg_cobros_index = Permission.permiso_new(name="reg_cobros_index")
    reg_cobros_new = Permission.permiso_new(name="reg_cobros_new")
    reg_cobros_destroy = Permission.permiso_new(name="reg_cobros_destroy")
    reg_cobros_update = Permission.permiso_new(name="reg_cobros_update")
    reg_cobros_show = Permission.permiso_new(name="reg_cobros_show")

    # Seed para Permisos modulo Registro Cobros
    content_index = Permission.permiso_new(name="content_index")
    content_new = Permission.permiso_new(name="content_new")
    content_destroy = Permission.permiso_new(name="content_destroy")
    content_update = Permission.permiso_new(name="content_update")
    content_show = Permission.permiso_new(name="content_show")

    # Seed de Roles
    tecnica = Role.role_new(
        name="Tecnica",
        permissions=[
            encuestre_index,
            encuestre_show,
            jya_index,
            jya_show,
            jya_update,
            jya_new,
            jya_destroy,
            reg_cobros_index,
            reg_cobros_show,
        ],
    )
    ecuestre = Role.role_new(
        name="Encuestre",
        permissions=[
            encuestre_index,
            encuestre_show,
            encuestre_update,
            encuestre_new,
            encuestre_destroy,
            jya_index,
            jya_show,
        ],
    )
    voluntario = Role.role_new(
        name="Voluntariado",
    )
    administracion = Role.role_new(
        name="Administracion",
        permissions=[
            team_index,
            team_show,
            team_update,
            team_new,
            team_destroy,
            reg_pagos_index,
            reg_pagos_show,
            reg_pagos_update,
            reg_pagos_new,
            reg_pagos_destroy,
            encuestre_index,
            encuestre_show,
            reg_cobros_index,
            reg_cobros_show,
            reg_cobros_update,
            reg_cobros_new,
            reg_cobros_destroy,
            jya_index,
            jya_show,
            jya_update,
            jya_new,
            jya_destroy,
            content_index,
            content_new,
            content_update,
            content_show,
            content_destroy
        ],
    )
    system_admin = Role.role_new(
        name="SystemAdmin",
        permissions=[
            user_index,
            user_new,
            user_destroy,
            user_update,
            user_show,
            user_block,
            user_update_password,
        ],
    )
    editor = Role.role_new(
        name="Editor",
        permissions=[
            content_index,
            content_new,
            content_update,
            content_show,
        ],
    )

    # Seed de Usuarios
    user_system_admin = User.user_new(
        email="admin@admin.com",
        alias="admin",
        password="admin",
        isActive=True,
        roles=[system_admin],
    )
    user_administracion = User.user_new(
        email="giuliana@gmail.com",
        alias="giu",
        password="123",
        isActive=True,
        roles=[administracion],
    )
    user_tecnica_ecuestre = User.user_new(
        email="lau@gmail.com",
        alias="lau",
        password="123",
        isActive=True,
        roles=[tecnica, ecuestre],
    )
    user_todo = User.user_new(
        email="eze@gmail.com",
        alias="eze",
        password="123",
        isActive=True,
        roles=[tecnica, ecuestre, voluntario, administracion, system_admin],
    )
    user_editor = User.user_new(
        email="weby@gmail.com",
        alias="weby",
        password="123",
        isActive=True,
        roles=[editor],
    )
    user_list = [user_system_admin, user_administracion, user_tecnica_ecuestre, user_todo, user_editor]

    # randoms
    for i in range(30):
        user = User.user_new(
            email=fake.email(),
            alias=fake.user_name(),
            password=fake.password(),
            isActive=True,
            roles=[random.choice([tecnica, ecuestre, voluntario, administracion, system_admin])],
        )
        user_list.append(user)

    return user_list


def _seed_professions():
    docente = professions.profession_new(name="Docente", description="Enseñanza")
    psicologo = professions.profession_new(
        name="Psicólogo/a",
        description="Especialista en salud mental que evalúa y trata trastornos emocionales para el bienestar del paciente.",
    )
    psicomotricista = professions.profession_new(
        name="Psicomotricista",
        description="Promueve el desarrollo motriz y la coordinación a través de actividades físicas y lúdicas.",
    )
    medico = professions.profession_new(
        name="Médico/a",
        description="Profesional de la salud que diagnostica y trata enfermedades, enfocándose en la prevención y el cuidado integral.",
    )
    kinesiologo = professions.profession_new(
        name="Kinesiólogo/a",
        description="Utiliza técnicas de movimiento para mejorar la movilidad y función física en rehabilitación.",
    )
    terapista_ocupacional = professions.profession_new(
        name="Terapista Ocupacional",
        description="Ayuda a mantener habilidades para la vida diaria, enfocándose en ocupaciones significativas.",
    )
    psicopedagogo = professions.profession_new(
        name="Psicopedagogo/a",
        description="Educador que aborda dificultades educativas y promueve el desarrollo integral del estudiante.",
    )
    docente = professions.profession_new(
        name="Docente",
        description="Facilita el aprendizaje y desarrollo de habilidades en estudiantes mediante diversas metodologías.",
    )
    profesor = professions.profession_new(
        name="Profesor",
        description="Enseña materias específicas, promoviendo conocimientos y habilidades a través de estrategias efectivas.",
    )
    fonoaudiologo = professions.profession_new(
        name="Fonoaudiólogo/a",
        description="Diagnostica y trata trastornos de comunicación y lenguaje, mejorando la deglución y la voz.",
    )
    veterinario = professions.profession_new(
        name="Veterinario/a",
        description="Cuidado y tratamiento de enfermedades en animales, promoviendo su bienestar y prevención.",
    )
    otro = professions.profession_new(
        name="Otro",
        description="Otras profesiones diversas no mencionadas en diferentes áreas y especialidades.",
    )

    administrativo = professions.job_new(
        name="Administrativo/a",
        description="Gestiona tareas administrativas en oficinas, asegurando la eficiencia operativa diaria.",
    )
    terapeuta = professions.job_new(
        name="Terapeuta",
        description="Facilita procesos de sanación y desarrollo personal mediante técnicas terapéuticas.",
    )
    conductor = professions.job_new(
        name="Conductor",
        description="Monta caballos y se encarga de su manejo durante el transporte y las actividades diarias.",
    )
    auxiliar_pista = professions.job_new(
        name="Auxiliar de pista",
        description="Asiste en la gestión y cuidado de caballos en pistas de equitación, garantizando seguridad.",
    )
    herrero = professions.job_new(
        name="Herrero",
        description="Artesano que forja metales, creando herramientas y piezas personalizadas a medida.",
    )
    veterinario = professions.job_new(
        name="Veterinario",
        description="Diagnostica y trata enfermedades en animales, ofreciendo cuidados preventivos y educativos.",
    )
    entrenador_caballos = professions.job_new(
        name="Entrenador de Caballos",
        description="Forma y entrena caballos para competencias o trabajo, desarrollando habilidades específicas.",
    )
    domador = professions.job_new(
        name="Domador",
        description="Adiestra caballos para establecer confianza y control entre el animal y el jinete.",
    )
    profesor_equitacion = professions.job_new(
        name="Profesor de Equitación",
        description="Enseña técnicas de monta y manejo de caballos, promoviendo seguridad en la práctica.",
    )
    auxiliar_mantenimiento = professions.job_new(
        name="Auxiliar de mantenimiento",
        description="Realiza mantenimiento preventivo y correctivo en instalaciones para asegurar su óptimo funcionamiento.",
    )

    jobs_list = [
        administrativo,
        terapeuta,
        conductor,
        auxiliar_pista,
        herrero,
        veterinario,
        entrenador_caballos,
        domador,
        profesor_equitacion,
        auxiliar_mantenimiento,
    ]

    professions_list = [
        docente,
        psicologo,
        psicomotricista,
        medico,
        kinesiologo,
        terapista_ocupacional,
        psicopedagogo,
        docente,
        profesor,
        fonoaudiologo,
        veterinario,
        otro,
    ]

    return jobs_list, professions_list


def _seed_localities():
    province_buenos_aires = adressing.province_new(name="Buenos Aires")
    province_caba = adressing.province_new(name="CABA")
    province_catamarca = adressing.province_new(name="Catamarca")
    province_chaco = adressing.province_new(name="Chaco")
    province_chubut = adressing.province_new(name="Chubut")
    province_cordoba = adressing.province_new(name="Córdoba")
    province_corrientes = adressing.province_new(name="Corrientes")
    province_entre_rios = adressing.province_new(name="Entre Ríos")
    province_formosa = adressing.province_new(name="Formosa")
    province_jujuy = adressing.province_new(name="Jujuy")
    province_la_pampa = adressing.province_new(name="La Pampa")
    province_la_rioja = adressing.province_new(name="La Rioja")
    province_mendoza = adressing.province_new(name="Mendoza")
    province_misiones = adressing.province_new(name="Misiones")
    province_neuquen = adressing.province_new(name="Neuquén")
    province_rio_negro = adressing.province_new(name="Río Negro")
    province_salta = adressing.province_new(name="Salta")
    province_san_juan = adressing.province_new(name="San Juan")
    province_san_luis = adressing.province_new(name="San Luis")
    province_santa_cruz = adressing.province_new(name="Santa Cruz")
    province_santa_fe = adressing.province_new(name="Santa Fe")
    province_santiago_del_estero = adressing.province_new(name="Santiago del Estero")
    province_tierra_del_fuego = adressing.province_new(name="Tierra del Fuego")
    province_tucuman = adressing.province_new(name="Tucumán")

    localities = [
        ("Berisso", province_buenos_aires),
        ("Ensenada", province_buenos_aires),
        ("La Plata", province_buenos_aires),
        ("25 de Mayo", province_buenos_aires),
        ("3 de febrero", province_buenos_aires),
        ("A. Alsina", province_buenos_aires),
        ("A. Gonzáles Cháves", province_buenos_aires),
        ("Aguas Verdes", province_buenos_aires),
        ("Alberti", province_buenos_aires),
        ("Arrecifes", province_buenos_aires),
        ("Ayacucho", province_buenos_aires),
        ("Azul", province_buenos_aires),
        ("Bahía Blanca", province_buenos_aires),
        ("Balcarce", province_buenos_aires),
        ("Baradero", province_buenos_aires),
        ("Benito Juárez", province_buenos_aires),
        ("Bolívar", province_buenos_aires),
        ("Bragado", province_buenos_aires),
        ("Brandsen", province_buenos_aires),
        ("Campana", province_buenos_aires),
        ("Cañuelas", province_buenos_aires),
        ("Capilla del Señor", province_buenos_aires),
        ("Capitán Sarmiento", province_buenos_aires),
        ("Carapachay", province_buenos_aires),
        ("Carhue", province_buenos_aires),
        ("Cariló", province_buenos_aires),
        ("Carlos Casares", province_buenos_aires),
        ("Carlos Tejedor", province_buenos_aires),
        ("Carmen de Areco", province_buenos_aires),
        ("Carmen de Patagones", province_buenos_aires),
        ("Castelli", province_buenos_aires),
        ("Chacabuco", province_buenos_aires),
        ("Chascomús", province_buenos_aires),
        ("Chivilcoy", province_buenos_aires),
        ("Colón", province_buenos_aires),
        ("Coronel Dorrego", province_buenos_aires),
        ("Coronel Pringles", province_buenos_aires),
        ("Coronel Rosales", province_buenos_aires),
        ("Coronel Suarez", province_buenos_aires),
        ("Costa Azul", province_buenos_aires),
        ("Costa Chica", province_buenos_aires),
        ("Costa del Este", province_buenos_aires),
        ("Costa Esmeralda", province_buenos_aires),
        ("Daireaux", province_buenos_aires),
        ("Darregueira", province_buenos_aires),
        ("Del Viso", province_buenos_aires),
        ("Dolores", province_buenos_aires),
        ("Don Torcuato", province_buenos_aires),
        ("Escobar", province_buenos_aires),
        ("Exaltación de la Cruz", province_buenos_aires),
        ("Florentino Ameghino", province_buenos_aires),
        ("Garín", province_buenos_aires),
        ("Gral. Alvarado", province_buenos_aires),
        ("Gral. Alvear", province_buenos_aires),
        ("Gral. Arenales", province_buenos_aires),
        ("Gral. Belgrano", province_buenos_aires),
        ("Gral. Guido", province_buenos_aires),
        ("Gral. Lamadrid", province_buenos_aires),
        ("Gral. Las Heras", province_buenos_aires),
        ("Gral. Lavalle", province_buenos_aires),
        ("Gral. Madariaga", province_buenos_aires),
        ("Gral. Pacheco", province_buenos_aires),
        ("Gral. Paz", province_buenos_aires),
        ("Gral. Pinto", province_buenos_aires),
        ("Gral. Pueyrredón", province_buenos_aires),
        ("Gral. Rodríguez", province_buenos_aires),
        ("Gral. Viamonte", province_buenos_aires),
        ("Gral. Villegas", province_buenos_aires),
        ("Guaminí", province_buenos_aires),
        ("Guernica", province_buenos_aires),
        ("Hipólito Yrigoyen", province_buenos_aires),
        ("Ing. Maschwitz", province_buenos_aires),
        ("Junín", province_buenos_aires),
        ("Laprida", province_buenos_aires),
        ("Las Flores", province_buenos_aires),
        ("Las Toninas", province_buenos_aires),
        ("Leandro N. Alem", province_buenos_aires),
        ("Lincoln", province_buenos_aires),
        ("Loberia", province_buenos_aires),
        ("Lobos", province_buenos_aires),
        ("Los Cardales", province_buenos_aires),
        ("Los Toldos", province_buenos_aires),
        ("Lucila del Mar", province_buenos_aires),
        ("Luján", province_buenos_aires),
        ("Magdalena", province_buenos_aires),
        ("Maipú", province_buenos_aires),
        ("Mar Chiquita", province_buenos_aires),
        ("Mar de Ajó", province_buenos_aires),
        ("Mar de las Pampas", province_buenos_aires),
        ("Mar del Plata", province_buenos_aires),
        ("Mar del Tuyú", province_buenos_aires),
        ("Marcos Paz", province_buenos_aires),
        ("Mercedes", province_buenos_aires),
        ("Miramar", province_buenos_aires),
        ("Monte", province_buenos_aires),
        ("Monte Hermoso", province_buenos_aires),
        ("Munro", province_buenos_aires),
        ("Navarro", province_buenos_aires),
        ("Necochea", province_buenos_aires),
        ("Olavarría", province_buenos_aires),
        ("Partido de la Costa", province_buenos_aires),
        ("Pehuajó", province_buenos_aires),
        ("Pellegrini", province_buenos_aires),
        ("Pergamino", province_buenos_aires),
        ("Pigüé", province_buenos_aires),
        ("Pila", province_buenos_aires),
        ("Pilar", province_buenos_aires),
        ("Pinamar", province_buenos_aires),
        ("Pinar del Sol", province_buenos_aires),
        ("Polvorines", province_buenos_aires),
        ("Pte. Perón", province_buenos_aires),
        ("Puán", province_buenos_aires),
        ("Punta Indio", province_buenos_aires),
        ("Ramallo", province_buenos_aires),
        ("Rauch", province_buenos_aires),
        ("Rivadavia", province_buenos_aires),
        ("Rojas", province_buenos_aires),
        ("Roque Pérez", province_buenos_aires),
        ("Saavedra", province_buenos_aires),
        ("Saladillo", province_buenos_aires),
        ("Salliqueló", province_buenos_aires),
        ("Salto", province_buenos_aires),
        ("San Andrés de Giles", province_buenos_aires),
        ("San Antonio de Areco", province_buenos_aires),
        ("San Antonio de Padua", province_buenos_aires),
        ("San Bernardo", province_buenos_aires),
        ("San Cayetano", province_buenos_aires),
        ("San Clemente del Tuyú", province_buenos_aires),
        ("San Nicolás", province_buenos_aires),
        ("San Pedro", province_buenos_aires),
        ("San Vicente", province_buenos_aires),
        ("Santa Teresita", province_buenos_aires),
        ("Suipacha", province_buenos_aires),
        ("Tandil", province_buenos_aires),
        ("Tapalqué", province_buenos_aires),
        ("Tordillo", province_buenos_aires),
        ("Tornquist", province_buenos_aires),
        ("Trenque Lauquen", province_buenos_aires),
        ("Tres Lomas", province_buenos_aires),
        ("Villa Gesell", province_buenos_aires),
        ("Villarino", province_buenos_aires),
        ("Zárate", province_buenos_aires),
        ("Palermo", province_caba),
        ("Recoleta", province_caba),
        ("Belgrano", province_caba),
        ("San Fernando del Valle", province_catamarca),
        ("Valle Viejo", province_catamarca),
        ("Tinogasta", province_catamarca),
        ("Resistencia", province_chaco),
        ("Sáenz Peña", province_chaco),
        ("Villa Ángela", province_chaco),
        ("Comodoro Rivadavia", province_chubut),
        ("Trelew", province_chubut),
        ("Puerto Madryn", province_chubut),
        ("Córdoba", province_cordoba),
        ("Villa Carlos Paz", province_cordoba),
        ("Río Cuarto", province_cordoba),
        ("Corrientes", province_corrientes),
        ("Goya", province_corrientes),
        ("Paso de los Libres", province_corrientes),
        ("Paraná", province_entre_rios),
        ("Concordia", province_entre_rios),
        ("Gualeguaychú", province_entre_rios),
        ("Formosa", province_formosa),
        ("Clorinda", province_formosa),
        ("Pirané", province_formosa),
        ("San Salvador de Jujuy", province_jujuy),
        ("Palpalá", province_jujuy),
        ("Perico", province_jujuy),
        ("Santa Rosa", province_la_pampa),
        ("General Pico", province_la_pampa),
        ("Toay", province_la_pampa),
        ("La Rioja", province_la_rioja),
        ("Chilecito", province_la_rioja),
        ("Aimogasta", province_la_rioja),
        ("Mendoza", province_mendoza),
        ("San Rafael", province_mendoza),
        ("Godoy Cruz", province_mendoza),
        ("Posadas", province_misiones),
        ("Oberá", province_misiones),
        ("Eldorado", province_misiones),
        ("Neuquén", province_neuquen),
        ("San Martín de los Andes", province_neuquen),
        ("Plottier", province_neuquen),
        ("Viedma", province_rio_negro),
        ("Bariloche", province_rio_negro),
        ("Cipolletti", province_rio_negro),
        ("Salta", province_salta),
        ("Tartagal", province_salta),
        ("Orán", province_salta),
        ("San Juan", province_san_juan),
        ("Rawson", province_san_juan),
        ("Chimbas", province_san_juan),
        ("San Luis", province_san_luis),
        ("Villa Mercedes", province_san_luis),
        ("Merlo", province_san_luis),
        ("Río Gallegos", province_santa_cruz),
        ("Caleta Olivia", province_santa_cruz),
        ("El Calafate", province_santa_cruz),
        ("Santa Fe", province_santa_fe),
        ("Rosario", province_santa_fe),
        ("Rafaela", province_santa_fe),
        ("Santiago del Estero", province_santiago_del_estero),
        ("La Banda", province_santiago_del_estero),
        ("Termas de Río Hondo", province_santiago_del_estero),
        ("Ushuaia", province_tierra_del_fuego),
        ("Río Grande", province_tierra_del_fuego),
        ("Tolhuin", province_tierra_del_fuego),
        ("San Miguel de Tucumán", province_tucuman),
        ("Tafí Viejo", province_tucuman),
        ("Concepción", province_tucuman),
    ]

    localities_list = []
    for locality_name, province in localities:
        locality = adressing.locality_new(name=locality_name, province=province)
        localities_list.append(locality)
    
    return localities_list


def _seed_disabilities():
    mental = disabilities.disability_type_new(name="Mental")
    motora = disabilities.disability_type_new(name="Motora")
    sensorial = disabilities.disability_type_new(name="Sensorial")
    visceral = disabilities.disability_type_new(name="Visceral")

    disabilities_list = []

    disabilities_list.append(disabilities.disability_diagnosis_new(name="ECNE, Lesión post-traumática", type=motora))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Mielomeningocele", type=motora))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Esclerosis Múltiple", type=motora))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Escoliosis Leve", type=motora))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Secuelas de ACV", type=motora))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Discapacidad Intelectual", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Trastorno del Espectro Autista", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Trastorno del Aprendizaje", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Trastorno por Déficit de Atención/Hiperactividad", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Trastorno de la Comunicación", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Trastorno de Ansiedad", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Síndrome de Down", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Retraso Madurativo", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Psicosis", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Trastorno de Conducta", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Trastornos del ánimo y afectivos", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="Trastorno Alimentario", type=mental))
    disabilities_list.append(disabilities.disability_diagnosis_new(name="OTRO", type=mental))

    return disabilities_list
    

def _seed_equestrian(members):
    activity1 = equestrian.activity_new(name="Hipoterapia")
    activity2 = equestrian.activity_new(name="Monta Terapéutica")
    activity3 = equestrian.activity_new(name="Deporte Ecuestre Adaptado")
    activity4 = equestrian.activity_new(name="Actividades Recreativas")
    activity5 = equestrian.activity_new(name="Equitación")

    list_activities = [activity1, activity2, activity3, activity4, activity5]

    horse_document_type1 = equestrian.horse_document_type_new(name="Ficha general")
    horse_document_type2 = equestrian.horse_document_type_new(name="Planificación de Entrenamiento")
    horse_document_type3 = equestrian.horse_document_type_new(name="Informe de Evolución")
    horse_document_type4 = equestrian.horse_document_type_new(name="Imágenes")
    horse_document_type5 = equestrian.horse_document_type_new(name="Registro veterinario")

    horses = []
    
    for i in range(30):
        horse = equestrian.horse_new(
            name=fake.first_name(),
            birth_date=fake.date_between(start_date="-2y", end_date="today"),
            gender=random.choice(["Macho", "Hembra"]),
            race=random.choice(
                [
                    "Norteño",
                    "Criollo",
                    "Árabe",
                    "Pura Sangre",
                    "Mestizo",
                    "Cuarto de Milla",
                    "Appaloosa",
                ]
            ),
            coat=random.choice(["Gris plateado", "Negro", "Marrón", "Blanco"]),
            donation=random.choice([True, False]),
            entry_date=fake.date_between(start_date="today", end_date="+2y"),
            assigned_members=random.sample(
                [member for member in members if member.job.id in [3, 7]],
                random.randint(1, 3),
            ),
            activities=random.sample(list_activities, random.randint(1, 5)),
            assigned_location=f"Sede {random.randint(0,15)}",
        )
        horses.append(horse)
    
    return horses


def _seed_members(localities):
    members = []
    for i in range(40):
        member = people.member_new(
            name=fake.first_name(),
            last_name=fake.last_name(),
            dni=f"{12345678 + i}",
            phone=f"123456789{i}",
            emergency_phone=f"987654321{i}",
            street="Calle Falsa",
            number=f"{123 + i}",
            locality=localities[random.randint(0, len(localities)-1)],
            email=f"{fake.first_name()}@gmail.com",
            start_date=fake.date_between(start_date="-2y", end_date="today"),
            end_date=None,
            health_insurance="OSDE",
            health_insurance_number=f"987654321{i}",
            condition="Personal Rentado",
            active=True,
            profession_id=random.randint(1, 12),
            job_id=random.randint(1, 10),
        )
        members.append(member)
    
    return members


def _seed_jya(members, localities, horses):
    jya_list = []
    for i in range(30):
        tutor1 = people.tutor_new(
            relationship="Padre",
            name=fake.first_name(),
            last_name=fake.last_name(),
            dni=f"{12345678 + i}",
            address="Calle Falsa 123",
            phone=f"123456789{i}",
            email=f"{fake.first_name()}@gmail.com",
            education_level="Universitario",
            job="Docente",
        )
        tutor2 = people.tutor_new(
            relationship="Madre",
            name=fake.first_name(),
            last_name=fake.last_name(),
            dni=f"{22345678 + i}",
            address="Calle Verdadera 456",
            phone=f"223456789{i}",
            email=f"{fake.first_name()}@gmail.com",
            education_level="Universitario",
            job="Enfermera",
        )
        jya = people.rider_new_seed(
            name=fake.first_name(),
            last_name=fake.last_name(),
            dni=f"{22345678 + i}",
            phone=f"223456789{i}",
            emergency_phone=f"287654321{i}",
            street="Calle Verdadera",
            number=f"{223 + i}",
            health_insurance="GALENO",
            health_insurance_number=f"287654321{i}",
            locality=localities[random.randint(0, len(localities)-1)],
            birth_date=fake.date_between(start_date="-100y", end_date="-4y"),
            grant_percentage=random.randint(1, 100),
            disability_id=random.randint(1, 18),
            family_allowance=random.choice([
            "Asignación universal por hijo",
            "Asignación universal por hijo con discapacidad",
            "Asignación por ayuda escolar anual"
            ]),
            pension_benefit=random.choice(["Nacional", "Provincial"]),
            has_guardianship=random.choice([True, False]),
            city_of_birth=localities[random.randint(0, len(localities)-1)],
            tutor_1_id=tutor1.id,
            tutor_2_id=tutor2.id,
            members=random.sample(
            [member for member in members if member.job.id in [2]],
            k=min(random.randint(1, 3), len([member for member in members if member.job.id in [2]]))  # Ensure sample size does not exceed population
            ),
        )
        school = people.school_new_seed(
            name=f"Escuela_{fake.last_name()}",
            address=f"Calle Falsa 12{i}",
            phone=f"12345678{i}",
            level=random.choice(["Inicial", "Primario", "Secundario", "Terciario", "Universitario"]),
            year=random.randint(1, 6),
            observations=f"Observaciones de la escuela {i}",
            rider=jya,
        )
        job_proposal = people.job_proposal_new_seed(
            institutional_work_proposal=random.choice([
                "Hipoterapia",
                "Monta Terapéutica",
                "Deporte Ecuestre Adaptado",
                "Actividades Recreativas",
                "Equitación"
            ]),
            condition="Regular",
            headquarters=random.choice(["CASJ", "HLP"]),
            days=[random.choice(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])],
            rider=jya,
            professor=random.choice([member for member in members if member.job.id in [9]]),
            member_horse_rider=random.choice([member for member in members if member.job.id in [3]]),
            horse=random.choice([horse for horse in horses]),
            assistant=random.choice([member for member in members if member.job.id in [4]]),
        )

        jya_list.append(jya)

    return jya_list


def _seed_cobros(jya_list, members):
    medio_pago_efectivo = registro_pagos_jya.medio_de_pago_new(tipo="Efectivo")
    medio_pago_tarjeta_credito = registro_pagos_jya.medio_de_pago_new(tipo="Tarjeta de Crédito")
    medio_pago_tarjeta_debito = registro_pagos_jya.medio_de_pago_new(tipo="Tarjeta de Débito")

    cobros = []
    for i in range(30):
        cobro = registro_pagos_jya.pago_jya_new(
            jinete_amazona=random.choice([jya for jya in jya_list]),
            medio_de_pago=random.choice([medio_pago_efectivo, medio_pago_tarjeta_credito, medio_pago_tarjeta_debito]),
            fecha_pago=generar_fecha_y_hora_aleatoria(fecha_inicio, fecha_fin),
            monto=random.randint(1000, 10000),
            observaciones=f"Cobro de prueba {i}",
            receptor=random.choice([member for member in members if member.job.id in [2]]),
            en_deuda=random.choice([True, False]),
        )
        cobros.append(cobro)
    
    return cobros


def _seed_pagos(jya_list, members):
    tipo1 = registro_pagos.tipo_new(tipo="Honorarios")
    tipo2 = registro_pagos.tipo_new(tipo="Proveedor")
    tipo3 = registro_pagos.tipo_new(tipo="Varios")

    pagos = []
    for i in range(30):
        tipo_pago = random.choice([tipo1, tipo2, tipo3])
        pago = registro_pagos.administracion_create(
            monto=2000 + i,
            beneficiario=random.choice([member for member in members]),
            tipo_pago=tipo_pago,
            fecha_pago=generar_fecha_y_hora_aleatoria(fecha_inicio, fecha_fin),
            descripcion=f"Pago de {tipo_pago.tipo}",
        )
        pagos.append(pago)
    
    return pagos

def _seed_articles(users):
    articles = []

    for i in range(29):
        # Genera contenido con formato Markdown aleatorio
        markdown_content = [
            f"### {fake.sentence()}",
            fake.sentence(),
            fake.text(max_nb_chars=100),
            f"* {fake.word()}\n* {fake.word()}\n* {fake.word()}",
            f"**{fake.sentence()}**",
            f"[Enlace a {fake.word()}]({fake.url()})"
        ]
        content = "\n".join(markdown_content)
                
        article = content_admin.create_article(
            form_data={
                'title': fake.sentence(),
                'summary': fake.text(max_nb_chars=255),
                'content': content,
                'author_id': random.choice(users).id,
                'status': random.choice(list(ArticleStatus))
            }
        )
        articles.append(article)

    return articles

def run():
    user_list = _seed_users()
    print("Usuarios creados con exito")
    jobs_list, professions_list = _seed_professions()
    print("Profesiones y trabajos creados con exito")
    localities_list = _seed_localities()
    print("Localidades creadas con exito")
    disabilities_list = _seed_disabilities()
    print("Discapacidades creadas con exito")
    members = _seed_members(localities_list)
    print("Miembros creados con exito")
    horses = _seed_equestrian(members)
    print("Caballos creados con exito")
    jya_list = _seed_jya(members, localities_list, horses)
    print("Jinetes y Amazonas creados con exito")
    cobros = _seed_cobros(jya_list, members)
    print("Cobros creados con exito")
    pagos = _seed_pagos(jya_list, members)
    print("Pagos creados con exito")
    articles = _seed_articles(user_list)
    print("Articulos creados con exito")
    print()
    print("Seeds ejecutadas con exito")
