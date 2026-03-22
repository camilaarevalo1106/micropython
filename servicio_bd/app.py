from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flasgger import Swagger
import os

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

# 🔥 CONEXIÓN A MONGODB
client = MongoClient(os.environ.get("mongodb+srv://admin:ca950624@cluster0.be2vy2z.mongodb.net/?mi_base_datos=Cluster0"))
db = client["mi_base_datos"]
coleccion = db["usuarios"]

# =========================
# CREATE (QUERY PARAMS)
# =========================
@app.route("/usuarios", methods=["POST"])
def insertar_usuario():
    """
    Insertar usuario
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
        description: Usuario insertado correctamente
    """
    try:
        nombre = request.args.get("nombre")
        edad = request.args.get("edad")

        if not nombre or not edad:
            return jsonify({"error": "Faltan parámetros"}), 400

        data = {
            "nombre": nombre,
            "edad": int(edad)
        }

        resultado = coleccion.insert_one(data)

        return jsonify({
            "mensaje": "Usuario insertado",
            "id": str(resultado.inserted_id)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# READ TODOS
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
    try:
        usuarios = []
        for u in coleccion.find():
            u["_id"] = str(u["_id"])
            usuarios.append(u)
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# READ UNO
# =========================
@app.route("/usuarios/<id>", methods=["GET"])
def obtener_usuario(id):
    """
    Obtener usuario por ID
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Usuario encontrado
    """
    try:
        usuario = coleccion.find_one({"_id": ObjectId(id)})
        if usuario:
            usuario["_id"] = str(usuario["_id"])
            return jsonify(usuario)
        return jsonify({"mensaje": "No encontrado"}), 404
    except:
        return jsonify({"mensaje": "ID inválido"}), 400


@app.route("/")
def inicio():
    return "Microservicio BD con Swagger 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)