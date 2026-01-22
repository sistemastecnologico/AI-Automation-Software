import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Configuración del cliente con el nombre de variable estándar
# ASEGÚRATE de que en Render el nombre sea: GROQ_API_KEY
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

@app.route("/")
def index():
    # Carga tu portafolio de billonario con los $10,000.00
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje")
        
        if not mensaje:
            return jsonify({"respuesta": "Escribe algo para poder ayudarte."})

        # MODELO ACTUALIZADO: llama-3.3-70b-versatile
        # El anterior (llama3-8b-8192) ya no funciona
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en finanzas y tecnología."},
                {"role": "user", "content": mensaje}
            ]
        )
        
        respuesta_ia = completion.choices[0].message.content
        return jsonify({"respuesta": respuesta_ia})
        
    except Exception as e:
        print(f"Error crítico: {e}")
        return jsonify({"respuesta": f"Error de conexión: Verifica que GROQ_API_KEY esté bien en Render."})

if __name__ == "__main__":
    # Puerto dinámico para Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)