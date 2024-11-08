from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.core.people.member_rider import Rider
from src.core.disabilities import DisabilityDiagnosis
from src.core.database import db
from src.web.handlers.autenticacion import check_permission, login_required
from src.web.handlers.error import unauthorized

bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@bp.get("/")
@login_required
def index():
    return render_template('statistics/index.html')


@bp.get("/disabilities")
@login_required
def disabilities():
    # if not check_permission('statistics'):
    #     return unauthorized()

    disabilities_list = db.session.query(
        DisabilityDiagnosis, db.func.count(Rider.disability_id).label('count')
    ).join(Rider, DisabilityDiagnosis.id == Rider.disability_id).group_by(
        DisabilityDiagnosis.id
    ).order_by(
        db.desc('count')
    ).all()

    # Preparar datos para la vista
    labels = [item.DisabilityDiagnosis.name for item in disabilities_list]
    counts = [item.count for item in disabilities_list]

    return render_template('statistics/disabilities.html', labels=labels, counts=counts)
