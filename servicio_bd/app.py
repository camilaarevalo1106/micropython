from flask import Flask, request, jsonify
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
# CREATE
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
        description: Usuario insertado
    """
    try:
        nombre = request.args.get("nombre")
        correo = request.args.get("correo")
        edad = request.args.get("edad")
        interes = request.args.get("interes")

        if not all([nombre, correo, edad, interes]):
            return jsonify({"error": "Faltan parámetros"}), 400

        data = {
            "nombre": nombre,
            "correo": correo,
            "edad": int(edad),
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
    usuarios = []
    for u in coleccion.find():
        u["_id"] = str(u["_id"])
        usuarios.append(u)
    return jsonify(usuarios)


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