from flask import Flask, jsonify
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

# 🔗 URL del microservicio BD
URL_BD = os.environ.get("URL_BD")

# =========================
# RECIBIR Y ENVIAR (PATH PARAMS)
# =========================
@app.route("/usuarios/<nombre>/<correo>/<int:edad>/<interes>", methods=["GET"])
def recibir_usuario(nombre, correo, edad, interes):
    """
    Enviar usuario al microservicio BD
    ---
    parameters:
      - name: nombre
        in: path
        type: string
        required: true
      - name: correo
        in: path
        type: string
        required: true
      - name: edad
        in: path
        type: integer
        required: true
      - name: interes
        in: path
        type: string
        required: true
    responses:
      200:
        description: Usuario enviado correctamente
    """
    try:
        url = f"{URL_BD}/usuarios/{nombre}/{correo}/{edad}/{interes}"

        respuesta = requests.get(url)

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