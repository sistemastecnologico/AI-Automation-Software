import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Conexión con la llave que pusiste en Render
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje")
        
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": mensaje}]
        )
        
        # AQUÍ ESTABA EL ERROR. ESTO YA ESTÁ CORREGIDO:
        respuesta_ia = completion.choices[0].message.content
        return jsonify({"respuesta": respuesta_ia})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"respuesta": "Error de conexión con Groq. Revisa la API KEY en Render."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))