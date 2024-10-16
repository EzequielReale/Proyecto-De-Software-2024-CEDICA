import pytest
from flask import Flask
from src.web.controllers.team import bp as team_bp

@pytest.fixture
def app():
    app = Flask(__name__, template_folder='src/web/templates')
    app.register_blueprint(team_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client, mocker):
    # Crear un mock de Member que incluye los atributos necesarios
    mock_person = mocker.Mock()
    mock_person.name = "Giuliana"
    mock_person.last_name = "Rossi"
    mock_person.dni = "12345678"
    mock_person.phone = "123456789"
    mock_person.emergency_phone = "987654321"
    mock_person.address = "Calle Falsa 123"
    mock_person.province_id = 1
    mock_person.locality_id = 1

    mock_member = mocker.Mock()
    mock_member.id = 1
    mock_member.email = "giuliana@gmail.com"
    mock_member.start_date = "2023-01-01"
    mock_member.end_date = "2023-12-31"
    mock_member.health_insurance = "Health Inc."
    mock_member.health_insurance_number = "987654321"
    mock_member.condition = "Voluntario"
    mock_member.active = True
    mock_member.profession_id = 1
    mock_member.person = mock_person  # Asignar la instancia de la persona al miembro

    # Hacer que list_members retorne la lista de miembros mockeados
    mocker.patch('src.core.people.list_members', return_value=[mock_member])
    
    # Hacer la solicitud GET a la ruta /team/
    response = client.get('/team/')
    
    # Comprobar el código de estado y los datos de la respuesta
    assert response.status_code == 200
    assert b'Giuliana Rossi' in response.data
    assert b'giuliana@gmail.com' in response.data
