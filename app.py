import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)
# Conexión profesional con Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    # Carga el dashboard visual negro
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje", "").lower()
        
        # IA de texto para estrategias de mercado
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": mensaje}]
        )
        respuesta_texto = completion.choices[0].message.content
        
        # Lógica de imágenes legales: si pides "grafico" o "visual", el sistema responde con datos
        return jsonify({"respuesta": respuesta_texto})
        
    except Exception as e:
        return jsonify({"respuesta": f"Error del sistema: {str(e)}"}), 500

if __name__ == "__main__":
    # Configuración de puerto obligatoria para Render (Logs 10:41)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)