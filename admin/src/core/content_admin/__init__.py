from src.core.content_admin.article import Article
from src.core.content_admin.article_status_enum import ArticleStatus
from src.core.database import db
from datetime import datetime

def list_articles(limit: int = 10, page: int = 1):
    """Devuelve todos los artículos de la BD con paginación"""

    paginated_query = Article.query.paginate(page=page, per_page=limit, error_out=False)
    return paginated_query.items, paginated_query.pages

def get_article_by_id(article_id: int):
    """Devuelve un artículo por su ID"""

    return Article.query.get(article_id)

def create_article(title: str, summary: str, content: str, author_id: int, status: ArticleStatus):
    """Crea un nuevo artículo"""

    new_article = Article(title=title, summary=summary, content=content, author_id=author_id, status=status if status else ArticleStatus.BORRADOR)
    
    if not status:
        new_article.status = ArticleStatus.BORRADOR
    else:
        new_article.status = status
        new_article.published_at = datetime.now()

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

def delete_article(article_id: int):
    """Elimina un artículo"""

    article = get_article_by_id(article_id)
    db.session.delete(article)
    db.session.commit()
    return article
