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
        "cedula": "1710034065",  # Ejemplo válido
        "nombre": "Carlos",
        "edad": 30,
        "sexo": "Masculino",
        "antecedentes": "Robo2018",
        "nivel_educativo": "Primaria6",
        "fecha": "1993-05-10"
    }
    response = client.post("/validar", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["mensaje"] == "Todos los datos son válidos"
