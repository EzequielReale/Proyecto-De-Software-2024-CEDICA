from src.core.database import db
from src.core.board.issue import Issue

def list_issues():
    """devuelve todos los reg de la bd """
    issues = Issue.query.all()
    return issues 

def create_issue(**kwargs):
    """ crea un issue, lo guarda en la bd y lo devuelve"""
    issue = Issue(**kwargs)
    db.session.add(issue)
    db.session.commit()

    return issue