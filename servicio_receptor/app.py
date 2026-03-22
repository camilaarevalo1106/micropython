from flask import Flask, request, jsonify
import requests
import os
from flasgger import Swagger

app = Flask(__name__)

# ✅ SWAGGER
app.config['SWAGGER'] = {
    'title': 'Microservicio Receptor',
    'uiversion': 3
}
app.config['JSON_SORT_KEYS'] = False

swagger = Swagger(app)

URL_BD = os.environ.get("URL_BD")

# =========================
# RECIBIR Y ENVIAR
# =========================
@app.route("/usuarios", methods=["POST"])
def recibir_usuario():
    """
    Recibir usuario y enviarlo al microservicio BD
    ---
    parameters:
      - name: nombre
        in: query
        type: string
        required: true
      - name: correo
        in: query
        type: string
        required: true
      - name: edad
        in: query
        type: integer
        required: true
      - name: interes
        in: query
        type: string
        required: true
    responses:
      200:
        description: Usuario enviado
    """
    try:
        nombre = request.args.get("nombre")
        correo = request.args.get("correo")
        edad = request.args.get("edad")
        interes = request.args.get("interes")

        if not all([nombre, correo, edad, interes]):
            return jsonify({"error": "Faltan parámetros"}), 400

        params = {
            "nombre": nombre,
            "correo": correo,
            "edad": edad,
            "interes": interes
        }

        respuesta = requests.post(f"{URL_BD}/usuarios", params=params)

        return jsonify({
            "mensaje": "Enviado correctamente",
            "respuesta_bd": respuesta.json()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def inicio():
    return "Microservicio receptor con Swagger 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)