from dataclasses import dataclass
from flask import render_template


@dataclass
class Error:
    code: int
    message: str
    description: str

def not_found(e):
    error = Error(404, "Not Found", "The requested URL was not found on the server.")
    return render_template("error.html", error=error), error.code


def unauthorized():
    """error de requerimiento sin autorizacion"""
    error = Error(401, "Unauthorized", "The server could not verify that you are authorized to access the URL requested.")
    return render_template("error.html", error=error), 401


def forbidden():
    """error que se muestra cuando quiere acceder a un permiso que no tiene"""
    error = Error(403, "Forbidden", "You don't have the permission to access the requested resource.")
    return render_template("error.html", error=error), 403