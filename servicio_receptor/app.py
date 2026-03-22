from flask import Flask, request, jsonify
import requests
import os
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, config={
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
})

# URL del microservicio BD
URL_BD = os.environ.get("URL_BD")

# =========================
# RECIBE Y REENVÍA
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
      - name: edad
        in: query
        type: integer
        required: true
    responses:
      200:
        description: Usuario enviado al microservicio BD
    """
    try:
        nombre = request.args.get("nombre")
        edad = request.args.get("edad")

        if not nombre or not edad:
            return jsonify({"error": "Faltan parámetros"}), 400

        params = {
            "nombre": nombre,
            "edad": edad
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