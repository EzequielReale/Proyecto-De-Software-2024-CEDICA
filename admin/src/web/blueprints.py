from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.equestrian import bp as equestrian_bp
from src.web.controllers.jya import bp as jya_bp
from web.controllers.resources import bp as resources_bp
from src.web.controllers.registro_pagos import bp as registro_pagos_bp
from src.web.controllers.team import bp as team_bp
from src.web.controllers.user import bp as user_bp
from src.web.controllers.articles import bp as articles_bp
from src.web.controllers.registro_pagos_jya import bp as registro_pagos_jya_bp
from src.web.controllers.messages import bp as internal_messages_bp

from src.web.controllers.statistics import bp as statistics_bp
from src.web.handlers import error

#api
from src.web.api.article import bp as api_article
from src.web.api.messages import bp as api_message



def register(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(registro_pagos_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(equestrian_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(jya_bp)
    app.register_blueprint(registro_pagos_jya_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(internal_messages_bp)
    app.register_blueprint(statistics_bp)
    #api
    app.register_blueprint(api_article)
    app.register_blueprint(api_message)


    app.register_error_handler(404, error.not_found)