from flask import Blueprint
from flask import render_template
from flask import request,redirect, flash,url_for

from flask import session
from src.core import equestrian
from src.core import people

bp=Blueprint("ecuestre",__name__,url_prefix="/ecuestre")

@bp.get("/")
def index():
    order_by = request.args.get('order_by', 'name')
    order = request.args.get('order', 'asc')
    limit = int(request.args.get('limit', 10))
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    activity_id = request.args.get('activity_id', type=int)
    
    horses, total_pages = equestrian.list_horses(order_by=order_by, order=order, limit=limit, page=page, search=search, activity_id=activity_id)
    
    return render_template("ecuestre/index.html", horses=horses, activities=equestrian.list_activities(), order_by=order_by, order=order, limit=limit, page=page, search=search, activity_id=activity_id, total_pages=total_pages)

@bp.get("/<int:id>")
def show(id: int):
    """Detalle de un caballo en específico"""
    horse = equestrian.get_horse_by_id(id)
    return render_template('ecuestre/show.html', horse=horse)

@bp.route("/create", methods=['GET', 'POST'])
def create():
    return render_template('ecuestre/create.html', activities=equestrian.list_activities(), members=people.list_members())

@bp.post("/<int:id>/delete")
def destroy(id: int):
    """Eliminar un caballo de la institución"""
    horse = equestrian.horse_delete(id)
    return redirect(url_for('ecuestre.index'))
