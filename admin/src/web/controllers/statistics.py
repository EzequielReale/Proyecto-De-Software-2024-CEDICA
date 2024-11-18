import io
from datetime import datetime

from flask import (
    Blueprint,
    flash,
    make_response,
    render_template,
    request,
    session,
)
import matplotlib.pyplot as plt

from src.core.statistics import (
    get_job_count,
    get_age_ranges,
    get_incomes_less_outflows,
    get_incomes_by_range,
    get_outflows_by_range,
    get_members_with_most_earnings,
    get_riders_with_debt,
)
from src.web.handlers.autenticacion import check_permission, login_required
from src.web.handlers.error import unauthorized

bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@bp.get("/")
@login_required
def index():
    """Renderiza la página de estadísticas"""
    if not check_permission(session, "reg_pagos_index") or not check_permission(session, "reg_cobros_index") or not check_permission(session, "team_index") or not check_permission(session, "jya_index"):
        return unauthorized()
    
    return render_template('statistics/index.html')


@bp.get("/balance")
@login_required
def balance():
    """Genera un gráfico de barras con el balance mensual de los últimos 12 meses"""
    if not check_permission(session, "reg_pagos_index") or not check_permission(session, "reg_cobros_index"):
        return unauthorized()

    month_labels, values = get_incomes_less_outflows()

    # Crear gráfico
    colors = ['lightgreen' if value >= 0 else 'red' for value in values]
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(month_labels, values, color=colors)
    ax.set_title('Balance mensual de CEDICA')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Monto')
    ax.set_xticks(range(len(month_labels)))
    ax.set_xticklabels(month_labels, rotation=45, ha="right", fontsize=10)
    ax.axhline(0, color='black', linewidth=0.8) # Línea horizontal en 0

    # Añadir labels en las barras para los valores
    for bar in bars:
        yval = bar.get_height()
        color = 'white' if yval < 0 else 'black'
        ax.text(bar.get_x() + bar.get_width() / 2, yval, f'${yval}', ha='center', va='bottom' if yval < 0 else 'top', color=color)

    fig.tight_layout()

    return to_image(fig)


@bp.get("/job")
@login_required
def job():
    """Genera un gráfico de barras horizontales con la cantidad de miembros del equipo en cada puesto laboral"""
    if not check_permission(session, "team_index"):
        return unauthorized()

    labels, values = get_job_count()

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title('Cantidad de miembros por puesto laboral')
    ax.barh(labels, values, color='orange')
    ax.set_xlabel('Cantidad de miembros')
    ax.set_ylabel('Puesto Laboral')
    fig.tight_layout()

    return to_image(fig)


@bp.get("/age")
@login_required
def age():
    """Genera un gráfico de torta con el porcentaje de jinetes/amazonas en el rango de edad de 3 a 18 años, 19 a 35 años, 36 a 50 años, 51 a 65 años y más de 65 años"""
    if not check_permission(session, "jya_index"):
        return unauthorized()
    
    labels, values = get_age_ranges()

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_title('Rango de edades de los Jinetes/Amazonas')
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    fig.tight_layout()

    return to_image(fig)


def to_image(fig):
    """Convierte un gráfico en una imagen"""
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    response = make_response(img.read())
    response.headers['Content-Type'] = 'image/png'

    return response


@bp.get("/most_earnings")
@login_required
def most_earnings():
    """Genera los reportes de los miembros con más ingresos"""
    if not check_permission(session, "reg_cobros_index"):
        return unauthorized()
    
    members = get_members_with_most_earnings()

    return render_template('statistics/most_earnings.html', members=members)


@bp.get("/debts")
@login_required
def debts():
    """Genera los reportes de los jinetes/amazonas con deudas"""
    if not check_permission(session, "reg_cobros_index"):
        return unauthorized()

    riders = get_riders_with_debt()

    return render_template('statistics/debts.html', riders=riders)


@bp.get("/balance_report")
@login_required
def balance_report():
    """Genera los reportes de los ingresos y egresos de CEDICA en el tiempo especificado"""
    if not check_permission(session, "reg_pagos_index") or not check_permission(session, "reg_cobros_index"):
        return unauthorized()
    
    incomes = []
    outflows = []
    filters = {
        'start_date': request.args.get('start_date'),
        'end_date': request.args.get('end_date') or datetime.today().strftime('%Y-%m-%d'),
    }

    if not filters['start_date']:
        flash('Ingrese una fecha de inicio (obligatorio) y de fin (opcional)', 'error')
    else:
        incomes = get_incomes_by_range(filters['start_date'], filters['end_date'])
        outflows = get_outflows_by_range(filters['start_date'], filters['end_date'])

    return render_template('statistics/balance_report.html', incomes=incomes, outflows=outflows, filters=filters)
