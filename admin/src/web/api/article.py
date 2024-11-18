from flask import Blueprint, request, jsonify
from src.core import content_admin
from src.web.schemas.article import articles_schema,article_filter_schema


bp = Blueprint("articles_api", __name__, url_prefix="/api")


@bp.get("/articles")
def list_articles():
    params = request.args.to_dict() #tomo parametros de la url, llegan como strings
    errors = article_filter_schema.validate(params)
    if errors:
        return jsonify({"error": "Parámetros inválidos o faltantes en la solicitud."}), 400

    author = params.get('author')
    published_from = params.get('published_from')
    published_to = params.get('published_to')
    page = int(params.get('page', 1))
    per_page = int(params.get('per_page', 10))
                
    query = content_admin.get_filtered_articles(author, published_from, published_to)
    paginated_articles = query.paginate(page=page, per_page=per_page, error_out=False)
       
    result = {
        "data": articles_schema.dump(paginated_articles.items),
        "page": paginated_articles.page,
        "per_page": paginated_articles.per_page,
        "total": paginated_articles.total
    }

    return jsonify(result), 200
