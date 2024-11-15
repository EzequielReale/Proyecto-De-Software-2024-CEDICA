import io
from datetime import datetime, timedelta

from flask import Blueprint, render_template, make_response
import matplotlib.pyplot as plt

from src.core.database import db
from src.core.professions import Job
from src.core.people.member_rider import Member, Rider
from src.core.registro_pagos import Pago
from src.core.registro_pagos_jya import PagoJineteAmazona
from src.web.handlers.autenticacion import check_permission, login_required
from src.web.handlers.error import unauthorized

bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@bp.get("/")
@login_required
def index():
    """Renderiza la página de estadísticas"""
    return render_template('statistics/index.html')


@bp.get("/balance")
@login_required
def balance():
    """Genera un gráfico de barras con el balance mensual de los últimos 12 meses"""
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

    # Crear gráfico
    colors = ['lightgreen' if value >= 0 else 'red' for value in values]
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(month_labels, values, color=colors)
    ax.set_xlabel('Mes')
    ax.set_ylabel('Monto')
    ax.set_xticks(month_labels)
    ax.set_xticklabels(month_labels, rotation=45, ha="right", fontsize=10)
    ax.axhline(0, color='black', linewidth=0.8) # Línea horizontal en 0

    # Añadir labels en las barras para los valores
    for bar in bars:
        yval = bar.get_height()
        color = 'white' if yval < 0 else 'black'
        ax.text(bar.get_x() + bar.get_width() / 2, yval, f'${yval}', ha='center', va='bottom' if yval < 0 else 'top', color=color)

    fig.tight_layout()

    # Convertir a imagen
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    response = make_response(img.read())
    response.headers['Content-Type'] = 'image/png'
    
    return response


@bp.get("/job")
@login_required
def job():
    """Genera un gráfico de barras horizontales con la cantidad de miembros del equipo en cada puesto laboral"""
    job_count = db.session.query(Job, db.func.count(Member.job_id).label('count')).join(Member, Job.id == Member.job_id).group_by(Job.id).all()
    
    labels = [item.Job.name for item in job_count]
    values = [item.count for item in job_count]

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(labels, values, color='orange')
    ax.set_xlabel('Cantidad de miembros')
    ax.set_ylabel('Puesto Laboral')
    fig.tight_layout()

    # Convertir a imagen
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    response = make_response(img.read())
    response.headers['Content-Type'] = 'image/png'

    return response


@bp.get("/age")
@login_required
def age():
    """Genera un gráfico de torta con el porcentaje de jinetes/amazonas en el rango de edad de 3 a 18 años, 19 a 35 años, 36 a 50 años, 51 a 65 años y más de 65 años"""
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

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    fig.tight_layout()

    # Convertir a imagen
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    response = make_response(img.read())
    response.headers['Content-Type'] = 'image/png'

    return response
