from src.core.database import db
from src.core.board.issue import Issue


def list_issues():
    """Devuelve todos los registros de la BD"""
    issues = Issue.query.all()
    return issues 

def create_issue(**kwargs):
    """Crea un issue, lo guarda en la BD y lo devuelve"""
    issue = Issue(**kwargs)
    db.session.add(issue)
    db.session.commit()

    return issue