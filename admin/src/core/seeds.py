from src.core import board, auth


def run():
    """Llena la base de datos con issues de prueba"""
    issue1 = board.create_issue(
        email="giu@gmail.com"
    )
    issue2= board.create_issue(
        email="yo@gmail.com"
    )
    user1 = auth.create_user(
        email="giuliana@gmail.com",
        password="123"
    )

