from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = 'bitcoin2026'
csrf = CSRFProtect(app)
CORS(app)

# CONFIGURACIÓN DE IA
API_KEY_REAL = "AIzaSyAFLGjZUy4E2qXYwRk3q4AwNbtNRWGk3c8"
genai.configure(api_key=API_KEY_REAL)
ia_brain = genai.GenerativeModel('gemini-1.5-flash')

# VARIABLES PROFESIONALES
balance_usd = 10000.00
donation_address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"

@app.route("/")
def dashboard():
    return render_template('dashboard.html', 
                           balance=balance_usd, 
                           donation_address=donation_address)

@app.route('/chat', methods=['POST'])
@csrf.exempt 
def chat():
    try:
        data = request.json
        pregunta = data.get("mensaje")
        contexto = "Eres una IA de ingeniería y medicina humanitaria de élite."
        response = ia_brain.generate_content(contexto + ": " + pregunta)
        return jsonify({"respuesta": response.text})
    except Exception as e:
        return jsonify({"respuesta": "Error en el cerebro de IA."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)