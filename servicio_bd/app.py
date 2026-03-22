from flask import Flask, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flasgger import Swagger
import os

app = Flask(__name__)

# ✅ SWAGGER
app.config['SWAGGER'] = {
    'title': 'Microservicio BD',
    'uiversion': 3
}
app.config['JSON_SORT_KEYS'] = False

swagger = Swagger(app)

# 🔥 MONGODB
client = MongoClient(os.environ.get("MONGO_URI"))
db = client["mi_base_datos"]
coleccion = db["usuarios"]

# =========================
# INSERTAR (PATH PARAMS)
# =========================
@app.route("/usuarios/<nombre>/<correo>/<int:edad>/<interes>", methods=["GET"])
def insertar_usuario(nombre, correo, edad, interes):
    """
    Insertar usuario
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
        description: Usuario insertado correctamente
    """
    try:
        data = {
            "nombre": nombre,
            "correo": correo,
            "edad": edad,
            "interes": interes
        }

        resultado = coleccion.insert_one(data)

        return jsonify({
            "mensaje": "Usuario insertado",
            "id": str(resultado.inserted_id)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# CONSULTAR TODOS
# =========================
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    """
    Obtener todos los usuarios
    ---
    responses:
      200:
        description: Lista de usuarios
    """
    usuarios = []
    for u in coleccion.find():
        u["_id"] = str(u["_id"])
        usuarios.append(u)
    return jsonify(usuarios)


@app.route("/")
def inicio():
    return "Microservicio BD con Swagger 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)