import re
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Función para validar la cédula de Ecuador o pasaporte
def validar_cedula(cedula):
    # Validación para cédula ecuatoriana
    if len(cedula) == 10 and cedula.isdigit():
        return validar_cedula_ecuadoriana(cedula)
    # Validación para pasaporte (alfanumérico)
    elif len(cedula) > 0 and len(cedula) <= 20 and re.match(r"^[a-zA-Z0-9]+$", cedula):
        return True  # Pasaporte válido
    return False

def validar_cedula_ecuadoriana(cedula):
    # Cálculo de la validación de la cédula ecuatoriana con el algoritmo de Módulo 10
    if len(cedula) != 10 or not cedula.isdigit():
        return False

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0

    for i in range(9):
        digito = int(cedula[i])
        coeficiente = coeficientes[i]
        resultado = digito * coeficiente
        if resultado > 9:
            resultado -= 9
        suma += resultado

    modulo_10 = suma % 10
    digito_verificador_calculado = 0 if modulo_10 == 0 else 10 - modulo_10
    return digito_verificador_calculado == int(cedula[9])

# Validación de los datos recibidos
def validar_datos(data):
    errores = []

    # Validar campos obligatorios
    campos_obligatorios = [
        "id_cedula", "nombre", "edad", "antecedentes_judiciales",
        "nivel_educativo", "fecha_nacimiento", "sexo"
    ]
    
    for campo in campos_obligatorios:
        if campo not in data or not data[campo]:
            errores.append(f"El campo '{campo}' es obligatorio.")

    
    # Validar la cédula
    if 'id_cedula' in data:
        if not validar_cedula(data['id_cedula']):
            errores.append("La cédula o pasaporte ingresado no es válido.")

    # Validar el nombre (solo letras)
    if 'nombre' in data and not re.match(r"^[a-zA-Z\s]+$", data['nombre']):
        errores.append("El nombre debe contener solo letras.")

    # Validar la edad (debe ser un número entero entre 0 y 100)
    if 'edad' in data and (not isinstance(data['edad'], int) or data['edad'] < 0 or data['edad'] > 100):
        errores.append("La edad debe ser un número entero entre 0 y 100.")

    # Validar antecedentes (alfanumérico, puede tener letras y números)
    if 'antecedentes_judiciales' in data and not re.match(r"^[a-zA-Z0-9\s]+$", data['antecedentes_judiciales']):
        errores.append("Los antecedentes deben ser alfanuméricos.")

    # Validar nivel educativo (combinación de letras y números, sin caracteres especiales)
    if 'nivel_educativo' in data and not re.match(r"^[a-zA-Z0-9\s]+$", data['nivel_educativo']):
        errores.append("El nivel educativo debe ser alfanumérico.")

    # Validar sexo (solo letras)
    if 'sexo' in data and not re.match(r"^[a-zA-Z]+$", data['sexo']):
        errores.append("El sexo debe ser solo letras (masculino o femenino).")

    # Validar la fecha de nacimiento (debe ser una fecha en el pasado y coherente con la edad)
    if 'fecha_nacimiento' in data:
        try:
            fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d')
            hoy = datetime.now()
            if fecha_nacimiento > hoy:
                errores.append("La fecha de nacimiento no puede ser en el futuro.")
            edad_calculada = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            if edad_calculada != data['edad']:
                errores.append("La edad no coincide con la fecha de nacimiento.")
        except ValueError:
            errores.append("La fecha de nacimiento debe estar en formato YYYY-MM-DD.")
    
    if 'familiares' in data:
        if not isinstance(data['familiares'], list):
            errores.append("El campo 'familiares' debe ser una lista.")
    else:
        for i, familiar in enumerate(data['familiares']):
            if 'id_cedula' not in familiar or 'nombre' not in familiar or 'parentesco' not in familiar:
                errores.append(f"Familiar en posición {i} no tiene los campos obligatorios (id_cedula, nombre, parentesco).")
            elif not validar_cedula(familiar['id_cedula']):
                errores.append(f"Cédula inválida en el familiar #{i+1}.")

    return errores

@app.route('/api/validar_recluso', methods=['POST'])
def validar_recluso():
    # Recibir los datos del recluso
    data = request.get_json()

    # Validar los datos
    errores = validar_datos(data)

    # Si hay errores, devolver el mensaje con todos los errores encontrados
    if errores:
        return jsonify({"errores": errores}), 400

    # Si los datos son válidos, devolver mensaje de éxito
    return jsonify({"mensaje": "Datos del recluso validados correctamente."}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)  # El microservicio de validación corre en el puerto 5001
