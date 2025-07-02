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
        "cedula": "1725279812",  # Ejemplo válido
        "nombre": "Carlos",
        "edad": 28,
        "sexo": "Masculino",
        "antecedentes": "Si",
        "nivel_educativo": "Bachillerato",
        "fecha": "1996-12-15"
    }
    response = client.post("/validar", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["mensaje"] == "Todos los datos son válidos"
