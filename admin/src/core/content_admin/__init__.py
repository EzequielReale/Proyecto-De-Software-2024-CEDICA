from src.core.content_admin.article import Article
from src.core.content_admin.article_status_enum import ArticleStatus
from src.core.database import db
from datetime import datetime
from dateutil import parser



def list_articles(limit: int = 10, page: int = 1):
    """Devuelve todos los artículos de la BD con paginación"""

    paginated_query = Article.query.order_by('id').paginate(page=page, per_page=limit, error_out=False)
    return paginated_query.items, paginated_query.pages

def get_article_by_id(article_id: int):
    """Devuelve un artículo por su ID"""

    return Article.query.get(article_id)

def create_article(form_data: dict):
    """Crea un nuevo artículo"""

    new_article = Article(**form_data)
    
    if not form_data.get('status'):
        new_article.status = ArticleStatus.BORRADOR
    else:
        new_article.published_at = datetime.now() if form_data.get('status') == ArticleStatus.PUBLICADO else None

    db.session.add(new_article)
    db.session.commit()
    return new_article

def update_article(article_id: int, title: str, summary: str, content: str, status: ArticleStatus):
    """Actualiza un artículo"""

    article = get_article_by_id(article_id)
    article.title = title
    article.summary = summary
    article.content = content
    article.status = status
    db.session.commit()
    return article

def update_article_status(article_id: int, status: ArticleStatus):
    """Actualiza el estado de un artículo"""

    article = get_article_by_id(article_id)
    article.status = status
    article.published_at = datetime.now() if status == ArticleStatus.PUBLICADO else None
    db.session.commit()
    return article

def delete_article(article_id: int):
    """Elimina un artículo"""

    article = get_article_by_id(article_id)
    db.session.delete(article)
    db.session.commit()
    return article


def get_filtered_articles(author, published_from, published_to):
    query = Article.query
    if author:
        query = query.join(Article.author).filter(User.alias.ilike(f"%{author}%"))
    if published_from:
        published_from =  parser.parse(published_from) #paso a datetime para hacer la consulta
        query = query.filter(Article.published_at >= published_from)
    if published_to:
        published_to = parser.parse(published_to)
        query = query.filter(Article.published_at <= published_to)
    return query
