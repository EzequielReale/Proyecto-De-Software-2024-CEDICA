from src.web.controllers.issues import bp as issues_bp
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.registro_pagos import bp as registro_pagos_bp
from src.web.controllers.team import bp as team_bp
from src.web.controllers.equestrian import bp as equestrian_bp
from src.web.handlers import error


def register(app):
    app.register_blueprint(issues_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(registro_pagos_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(equestrian_bp)

    app.register_error_handler(404, error.not_found)