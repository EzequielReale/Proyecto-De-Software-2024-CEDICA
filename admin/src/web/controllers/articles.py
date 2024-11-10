from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from src.core.user_role_permission.operations.user_operations import get_user_by_email
from src.core import content_admin as content
from src.core.content_admin.article_status_enum import ArticleStatus
from src.web.handlers.autenticacion import check_permission, login_required
from src.web.handlers.error import unauthorized

bp=Blueprint("articles",__name__, url_prefix="/articles")

@bp.get("/")
@login_required
def index():
    if not check_permission(session, "content_index"):
        return unauthorized()

    limit = int(request.args.get('limit', 6))
    page = int(request.args.get('page', 1))
    
    articles, total_pages = content.list_articles(limit=limit, page=page)
    
    return render_template("articles/index.html", articles=articles, article_status=ArticleStatus, limit=limit, page=page, total_pages=total_pages)

@bp.get("/<int:id>")
@login_required
def show(id: int):
    """Detalle de un artículo en específico"""
    if not check_permission(session,"content_show"):
        return unauthorized()
        
    res = content.get_article_by_id(id)
    return render_template('articles/show.html', article=res, article_status=ArticleStatus)

@bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if not check_permission(session,"content_new"):
        return unauthorized()
     
    # Si no se envía el formulario
    if request.method == 'GET':
        return render_template('articles/create.html')
    
    # Si se envía el formulario, se procede con la creación del artículo
    form_data = {
        'title': request.form.get('title'),
        'summary': request.form.get('summary'),
        'content': request.form.get('content'),
        'author_id': get_user_by_email(session["user"]).id,
        'status': ArticleStatus.BORRADOR if not request.form.get('status') else ArticleStatus.BORRADOR if request.form.get('status') == "0" else ArticleStatus.PUBLICADO,
    }

    # Validar los datos del formulario
    errors = validate_article_form(form_data)

    # Si hay errores, mostrar mensajes de error y renderizar el formulario nuevamente
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('articles/create.html', form_data=form_data)
    
    article = content.create_article(form_data)
    flash(f"Artículo creado exitosamente", "success")
    return redirect(url_for('articles.show', id=article.id))


@bp.route("/<int:id>/update", methods=['GET', 'POST'])
def update(id: int)->str:
    """Recibe el id de un artículo y muestra el formulario para editarlo, o lo actualiza en caso de que se envíe el formulario"""
    if not check_permission(session,"content_update"):
        return unauthorized()
     
    article = content.get_article_by_id(id)
    
    if not article:
        flash(f"El artículo con ID {id} no existe", "danger")
        return redirect(url_for('articles.index'))

    # Si se envía el formulario
    if request.method == 'POST':
        # Obtener los datos del formulario
        form_data = {
            'title': request.form.get('title'),
            'summary': request.form.get('summary'),
            'content': request.form.get('content'),
            'status': request.form.get('status')
        }

        # Validar los datos del formulario
        errors = validate_article_form(form_data)

        # Si hay errores, mostrar mensajes de error y renderizar el formulario nuevamente
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('articles/update.html', id=article.id, form_data=form_data, article_status=ArticleStatus)

        article_status = article.status

        if form_data['status'] == "0":
            article_status = ArticleStatus.BORRADOR
        elif form_data['status'] == "1":
            article_status = ArticleStatus.PUBLICADO
        else:
            article_status = ArticleStatus.ARCHIVADO 

        # Edición del artículo
        content.update_article(
            article_id=id,
            title=form_data['title'],
            summary=form_data['summary'],
            content=form_data['content'],
            status=article_status
        )
        
        flash(f"Artículo actualizado exitosamente", "success")
        return redirect(url_for('articles.index'))
    
        
    return render_template('articles/update.html', id=article.id, form_data=article, article_status=ArticleStatus)

@bp.post("/<int:id>/update_status/<int:status>")
@login_required
def update_status(id: int, status: int):
    """Actualiza el estado de un artículo según su ID"""
    if not check_permission(session,"content_update"):
        return unauthorized()
     
    if not content.get_article_by_id(id):
        flash(f"El artículo con ID {id} no existe", "danger")
        return redirect(url_for('articles.index'))

    article_status = ArticleStatus.BORRADOR

    if status == 0:
        article_status = ArticleStatus.BORRADOR
    elif status == 1:
        article_status = ArticleStatus.PUBLICADO
    else:
        article_status = ArticleStatus.ARCHIVADO 
    
    article = content.update_article_status(id, article_status)
    flash(f"Artículo {article.id} actualizado exitosamente", "success")
    return redirect(url_for('articles.show', id=article.id))

@bp.post("/<int:id>/delete")
@login_required
def destroy(id: int):
    """Elimina un artículo según su ID"""
    if not check_permission(session,"content_destroy"):
        return unauthorized()
     
    if not content.get_article_by_id(id):
        flash(f"El artículo con ID {id} no existe", "danger")
        return redirect(url_for('articles.index'))
     
    article = content.delete_article(id)
    flash(f"Artículo {article.id} eliminado exitosamente", "success")
    return redirect(url_for('articles.index'))

def validate_article_form(data):
    errors = []

    # Validar título
    if not data.get('title') or len(data['title']) > 255:
        errors.append("El título es obligatorio y debe tener menos de 255 caracteres.")
    
    # Validar copete
    if not data.get('summary') or len(data['summary']) > 255:
        errors.append("El copete es obligatorio y debe tener menos de 255 caracteres.")

    # Validar contenido
    if not data.get('content'):
        errors.append("Debe ingresar un contenido.")

    return errors
