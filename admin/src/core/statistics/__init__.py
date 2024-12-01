from datetime import datetime
from dateutil.relativedelta import relativedelta

from src.core.database import db
from src.core.professions import Job
from src.core.people import has_debt
from src.core.people.member_rider import Member, Rider
from src.core.registro_pagos import Pago
from src.core.registro_pagos_jya import PagoJineteAmazona


def get_job_count()->tuple[list[str], list[int]]:
    """Obtiene la cantidad de miembros por puesto laboral y retorna los labels y valores"""
    job_count = (
        db.session.query(Job, db.func.count(Member.job_id).label("count"))
        .join(Member, Job.id == Member.job_id)
        .group_by(Job.id)
        .all()
    )

    labels = [item.Job.name for item in job_count]
    values = [item.count for item in job_count]

    return labels, values


def get_age_ranges() -> tuple[list[str], list[int]]:
    """Obtiene la cantidad de jinetes/amazonas en el rango de edad de 3 a 18 años, 19 a 35 años, 36 a 50 años, 51 a 65 años y más de 65 años"""
    today = datetime.today()
    age_ranges = {
        '3-18': 0, '19-35': 0, '36-50': 0, '51-65': 0, '65+': 0
    }

    age_ranges['3-18'] = db.session.query(db.func.count(Rider.id)).filter(
        (today.year - db.extract('year', Rider.birth_date)) <= 18
    ).scalar()

    age_ranges['19-35'] = db.session.query(db.func.count(Rider.id)).filter(
        (today.year - db.extract('year', Rider.birth_date)) > 18,
        (today.year - db.extract('year', Rider.birth_date)) <= 35
    ).scalar()

    age_ranges['36-50'] = db.session.query(db.func.count(Rider.id)).filter(
        (today.year - db.extract('year', Rider.birth_date)) > 35,
        (today.year - db.extract('year', Rider.birth_date)) <= 50
    ).scalar()

    age_ranges['51-65'] = db.session.query(db.func.count(Rider.id)).filter(
        (today.year - db.extract('year', Rider.birth_date)) > 50,
        (today.year - db.extract('year', Rider.birth_date)) <= 65
    ).scalar()

    age_ranges['65+'] = db.session.query(db.func.count(Rider.id)).filter(
        (today.year - db.extract('year', Rider.birth_date)) > 65
    ).scalar()

    labels = list(age_ranges.keys())
    values = list(age_ranges.values())

    return labels, values


def get_months(start_date:datetime) -> list[str]:
    """Recibe fecha de inicio y retorna los meses (como fecha y como string con sus nombres traducidos)"""
    months = []
    month_labels = []
    for i in range(12):
        month_date = start_date + relativedelta(months=i)
        months.append(month_date.strftime('%Y-%m'))
        month_labels.append(month_date.strftime('%B %Y'))

    # Traduce los nombres de los meses
    month_translation = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
        'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
        'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 
        'December': 'Diciembre'
    }
    month_labels = [
        month_translation[label.split()[0]] + ' ' + label.split()[1] 
        for label in month_labels
    ]

    return months, month_labels


def get_incomes_less_outflows() -> tuple[list[str], list[int]]:
    """Obtiene los ingresos - egresos de CEDICA en los últimos 12 meses"""
    # Obtiene el primer día del mes actual
    current_month_start = datetime.today().replace(day=1)
    
    # Obtiene el primer día del mes hace 12 meses
    start_date = (current_month_start - relativedelta(months=11))

    # Genera los meses
    months, month_labels = get_months(start_date)

    # Consultas con rangos de fecha exactos
    income_records = (
        db.session.query(
            db.func.to_char(PagoJineteAmazona.fecha_pago, 'YYYY-MM').label('month'),
            db.func.sum(PagoJineteAmazona.monto).label('total_income')
        )
        .filter(
            PagoJineteAmazona.fecha_pago >= start_date,
            PagoJineteAmazona.fecha_pago < current_month_start + relativedelta(months=1),
            PagoJineteAmazona.en_deuda == False
        )
        .group_by('month')
        .all()
    )

    outflow_records = (
        db.session.query(
            db.func.to_char(Pago.fecha_pago, 'YYYY-MM').label('month'),
            db.func.sum(Pago.monto).label('total_outflow')
        )
        .filter(
            Pago.fecha_pago >= start_date,
            Pago.fecha_pago < current_month_start + relativedelta(months=1)
        )
        .group_by('month')
        .all()
    )

    # Convierte los resultados a diccionarios
    monthly_income = {record.month: record.total_income for record in income_records}
    monthly_outflow = {record.month: record.total_outflow for record in outflow_records}

    # Hace la resta mes a mes
    values = [
        monthly_income.get(month, 0) - monthly_outflow.get(month, 0)
        for month in months
    ]

    return month_labels, values


def get_riders_with_debt() -> list[dict]:
    """Obtiene a los jinetes y amazonas que tienen deuda"""
    today = datetime.today()
    
    riders_with_debt = db.session.query(
        Rider.id,
        Rider.name,
        Rider.last_name,
        Rider.dni,
        Rider.birth_date,
        Rider.phone,
        db.func.count(PagoJineteAmazona.id).label('cantidad_de_pagos_pendientes'),
        db.func.sum(PagoJineteAmazona.monto).label('monto_total_de_deuda')
    ).join(PagoJineteAmazona, Rider.id == PagoJineteAmazona.jinete_amazona_id)\
     .filter(PagoJineteAmazona.en_deuda == True)\
     .group_by(Rider.id, Rider.name, Rider.last_name, Rider.dni, Rider.birth_date, Rider.phone)\
     .order_by(Rider.last_name, Rider.name)\
     .all()
    
    result = [
        {
            'Nombre': rider.last_name + ' ' + rider.name,
            'DNI': rider.dni,
            'Edad': today.year - rider.birth_date.year,
            'Contacto': rider.phone,
            'Cantidad_de_pagos_pendientes': rider.cantidad_de_pagos_pendientes,
            'Monto_total_de_deuda': "$" + str(rider.monto_total_de_deuda)
        }
        for rider in riders_with_debt
    ]

    return result


def get_incomes_by_range(start_date:datetime, end_date:datetime)->list[PagoJineteAmazona]:
    """Obtiene los ingresos de CEDICA en un rango de fechas"""
    incomes = PagoJineteAmazona.query.filter(
        PagoJineteAmazona.fecha_pago.between(start_date, end_date),
        PagoJineteAmazona.en_deuda == False
    ).order_by(PagoJineteAmazona.fecha_pago.asc()).all()
    
    result = [
        {
            'Monto': "$" + str(income.monto),
            'Fecha': income.fecha_pago.strftime('%d/%m/%Y'),
            'Jinete_amazona': income.jinete_amazona.name + ' ' + income.jinete_amazona.last_name + ' (DNI: ' + income.jinete_amazona.dni + ')',
            'Receptor': income.receptor.name + ' ' + income.receptor.last_name + ' (DNI: ' + income.receptor.dni + ')'
        }
        for income in incomes
    ]
    
    return result


def get_outflows_by_range(start_date:datetime, end_date:datetime)->list[dict]:
    """Obtiene los egresos de CEDICA en un rango de fechas"""
    outflows = Pago.query.filter(Pago.fecha_pago.between(start_date, end_date)).order_by(Pago.fecha_pago.asc()).all()
    result = [
        {
            'Monto': "$" + str(outflow.monto),
            'Fecha': outflow.fecha_pago.strftime('%d/%m/%Y'),
            'Tipo': outflow.tipo_pago.tipo
        }
        for outflow in outflows
    ]
    return result


def get_members_with_most_earnings()->list[dict]:
    """Obtiene a los miembros con más ingresos"""
    member_earnings = db.session.query(
        Member.id,
        Member.name,
        Member.last_name,
        Member.dni,
        db.func.sum(PagoJineteAmazona.monto).label('total_earnings'),
        db.func.count(PagoJineteAmazona.id).label('total_payments')
    ).join(PagoJineteAmazona, Member.id == PagoJineteAmazona.receptor_id)\
     .group_by(Member.id, Member.name, Member.last_name, Member.dni)\
     .order_by(db.desc('total_earnings'))\
     .all()

    result = [
        {
            'Nombre': member.name + ' ' + member.last_name,
            'DNI': member.dni,
            'Total_recaudado': "$" + str(member.total_earnings),
            'Cantidad_de_pagos': member.total_payments
        }
        for member in member_earnings
    ]

    return result
