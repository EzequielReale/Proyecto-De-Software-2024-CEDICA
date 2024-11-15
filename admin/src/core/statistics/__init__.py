from datetime import datetime, timedelta
import os
import pandas as pd

from flask import send_file, after_this_request

from src.core.database import db
from src.core.professions import Job
from src.core.people import has_debt
from src.core.people.member_rider import Member, Rider
from src.core.registro_pagos import Pago
from src.core.registro_pagos_jya import PagoJineteAmazona
from fpdf import FPDF


def get_job_count()->tuple[list[str], list[int]]:
    """Obtiene la cantidad de miembros por puesto laboral y retorna los labels y valores"""
    job_count = db.session.query(Job, db.func.count(Member.job_id).label('count')).join(Member, Job.id == Member.job_id).group_by(Job.id).all()
    
    labels = [item.Job.name for item in job_count]
    values = [item.count for item in job_count]

    return labels, values


def get_age_ranges()->tuple[list[str], list[int]]:
    """Obtiene la cantidad de jinetes/amazonas en el rango de edad de 3 a 18 años, 19 a 35 años, 36 a 50 años, 51 a 65 años y más de 65 años"""
    today = datetime.today()
    age_ranges = {
        '3-18': 0, '19-35': 0, '36-50': 0, '51-65': 0, '65+': 0
    }
    for rider in Rider.query.all():
        age = today.year - rider.birth_date.year
        if age <= 18:
            age_ranges['3-18'] += 1
        elif age <= 35:
            age_ranges['19-35'] += 1
        elif age <= 50:
            age_ranges['36-50'] += 1
        elif age <= 65:
            age_ranges['51-65'] += 1
        else:
            age_ranges['65+'] += 1
    
    labels = list(age_ranges.keys())
    values = list(age_ranges.values())

    return labels, values


def get_incomes_less_outflows()->tuple[list[str], list[int]]:
    """Obtiene los ingresos - egresos de CEDICA en los últimos 12 meses"""
    # Obtiene la fecha actual y la fecha de inicio de los últimos 12 meses
    today = datetime.today()
    start_date = today.replace(day=1) - timedelta(days=365)

    # Crea una lista de los últimos 12 meses
    months = [(start_date + timedelta(days=30 * i)).strftime('%Y-%m') for i in range(13)]
    month_labels = [(start_date + timedelta(days=30 * i)).strftime('%B %Y') for i in range(13)]

    # Traduce los nombres de los meses al español
    month_translation = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
        'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
        'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
    }
    month_labels = [month_translation[label.split()[0]] + ' ' + label.split()[1] for label in month_labels]

    # Inicializar diccionarios para ingresos y egresos
    monthly_income = {month: 0 for month in months}
    monthly_outflow = {month: 0 for month in months}

    # Consultar ingresos y egresos mensuales
    income_records = db.session.query(PagoJineteAmazona.monto, PagoJineteAmazona.fecha_pago).filter(PagoJineteAmazona.fecha_pago >= start_date).all()
    outflow_records = db.session.query(Pago.monto, Pago.fecha_pago).filter(Pago.fecha_pago >= start_date).all()

    # Sumar ingresos y egresos a los diccionarios y calcular el balance mensual
    for record in income_records:
        month = record.fecha_pago.strftime('%Y-%m')
        if month in monthly_income:
            monthly_income[month] += record.monto

    for record in outflow_records:
        month = record.fecha_pago.strftime('%Y-%m')
        if month in monthly_outflow:
            monthly_outflow[month] += record.monto

    values = [monthly_income[month] - monthly_outflow[month] for month in months]

    return month_labels, values


def get_riders_with_debt()->list[dict]:
    """Obtiene a los jinetes y amazonas que tienen deuda"""
    today = datetime.today()
    riders = Rider.query.all()
    riders_with_debt = [rider for rider in riders if has_debt(rider.id)]
        
    result = [
        {
            'Nombre': rider.name + ' ' + rider.last_name,
            'DNI': rider.dni,
            'Edad': today.year - rider.birth_date.year,
            'Cantidad_de_pagos_pendientes': db.session.query(db.func.count(PagoJineteAmazona.id)).filter(
                PagoJineteAmazona.jinete_amazona_id == rider.id,
                PagoJineteAmazona.en_deuda == True
            ).scalar()
        }
        for rider in riders_with_debt
    ]

    return result


def get_incomes_by_range(start_date:datetime, end_date:datetime)->list[PagoJineteAmazona]:
    """Obtiene los ingresos de CEDICA en un rango de fechas"""
    incomes = PagoJineteAmazona.query.filter(
        PagoJineteAmazona.fecha_pago.between(start_date, end_date),
        PagoJineteAmazona.en_deuda == False
    ).all()
    
    result = [
        {
            'Monto': "$" + str(income.monto),
            'Fecha': income.fecha_pago.strftime('%d/%m/%Y'),
            'Jinete_amazona': income.jinete_amazona.name + ' ' + income.jinete_amazona.last_name + ' ' + income.jinete_amazona.dni,
            'Receptor': income.receptor.name + ' ' + income.receptor.last_name + ' ' + income.receptor.dni
        }
        for income in incomes
    ]
    
    return result


def get_outflows_by_range(start_date:datetime, end_date:datetime)->list[dict]:
    """Obtiene los egresos de CEDICA en un rango de fechas"""
    outflows = Pago.query.filter(Pago.fecha_pago.between(start_date, end_date)).all()
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


def make_report(data: list[dict], report_name: str):
    """Genera un reporte con las estadísticas de CEDICA en formato Excel"""
    df = pd.DataFrame(data)
        
    if not os.path.exists('reports'):
        os.makedirs('reports')
            
    file_path = f'reports/{report_name}.xlsx'
    df.to_excel(file_path, index=False)

    return file_path


def save_report(data: list[dict], report_name: str):
    """Guarda el reporte solicitado en Minio"""
    pass
