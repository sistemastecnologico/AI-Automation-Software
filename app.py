import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Esto lee la llave que pusiste en Render
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje")
        # Genera la respuesta directamente
        response = model.generate_content(mensaje)
        return jsonify({"respuesta": response.text})
    except Exception as e:
        print(f"Detalle del fallo: {e}")
        return jsonify({"respuesta": "El sistema está sincronizando con la red Solana..."})