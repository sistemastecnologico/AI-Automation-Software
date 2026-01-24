import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Esto fuerza a la web a mostrar el Dashboard sin buscar carpetas externas
HTML_FIX = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Elite Billionaire Terminal</title>
    <style>
        body { background-color: #000; color: #0f0; font-family: monospace; padding: 50px; text-align: center; }
        .box { border: 2px solid #0f0; padding: 30px; background: #050505; display: inline-block; border-radius: 15px; box-shadow: 0 0 15px #0f0; }
        .donate { background: #f39c12; color: #000; padding: 15px; font-weight: bold; border: none; border-radius: 5px; cursor: pointer; }
        input { background: #111; color: #fff; border: 1px solid #0f0; padding: 10px; width: 80%; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="box">
        <button class="donate">SOPORTE CRYPTO ACTIVO</button>
        <h1>SISTEMA IA DE ÉLITE LIVE</h1>
        <p>Consultoría técnica avanzada: Finanzas | Medicina | Ciencia</p>
        <div id="chat"></div>
        <input type="text" placeholder="Escriba su consulta técnica aquí...">
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    # El mimetype='text/html' es lo que quita el fondo blanco y el texto plano
    return Response(HTML_FIX, mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje", "")
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Eres un consultor de élite."}, {"role": "user", "content": mensaje}]
        )
        return jsonify({"respuesta": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"respuesta": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)