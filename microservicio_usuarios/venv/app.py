from flask import Flask, request, jsonify
from database import DatabaseConnection

app = Flask(__name__)
db = DatabaseConnection()

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.json
    cursor = db.get_cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, correo, telefono, tipo_usuario, contrasena)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """, (data['nombre'], data['apellido'], data['correo'], data['telefono'], data['tipo_usuario'], data['contrasena']))
        usuario_id = cursor.fetchone()['id']
        db.commit()
        return jsonify({"id": usuario_id}), 201
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
