import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_validar_cedula_ecuatoriana(client):
    payload = {
        "id_cedula": "1725279812",
        "nombre": "Carlos",
        "edad": 28,
        "sexo": "Masculino",
        "antecedentes_judiciales": "Robo2018",
        "nivel_educativo": "Bachillerato",
        "fecha_nacimiento": "1996-12-15"
    }
    response = client.post("/api/validar_recluso", json=payload)
    assert response.status_code == 200