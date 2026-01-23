import os
from flask import Flask, render_template, request, jsonify, session
from groq import Groq

app = Flask(__name__)
# Clave para asegurar las sesiones del sistema
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "billonario_key_2026")

# Conexión con el motor de IA Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    # Carga la interfaz del dashboard profesional
    return render_template("dashboard.html", user=session.get('user'))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        datos = request.json
        mensaje = datos.get("mensaje", "").lower()
        
        # FUNCIÓN PREMIUM: GENERACIÓN DE GRÁFICOS
        if "grafico" in mensaje or "balance" in mensaje:
            config = "{type:'bar',data:{labels:['Ene','Feb','Mar'],datasets:[{label:'Ganancias',data:[400,900,2400]}]}}"
            chart_url = f"https://quickchart.io/chart?c={config}".replace(" ", "")
            respuesta_ia = f"💹 **Análisis Visual**: Rendimiento optimizado.<br><img src='{chart_url}' width='100%' style='border-radius:10px; margin-top:10px;'>"
        
        # FUNCIÓN PREMIUM: CREACIÓN DE IMÁGENES CON IA
        elif "crea" in mensaje or "imagen" in mensaje:
            prompt = mensaje.replace("crea", "").strip().replace(" ", "%20")
            img_url = f"https://pollinations.ai/p/{prompt}?width=512&height=512&seed=42"
            respuesta_ia = f"🎨 **IA Generativa**: Activo visual creado:<br><img src='{img_url}' width='100%' style='border-radius:10px; margin-top:10px;'>"

        else:
            # Respuesta estándar de texto usando Llama 3
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": mensaje}]
            )
            respuesta_ia = completion.choices[0].message.content

        return jsonify({"respuesta": respuesta_ia})
    except Exception as e:
        # Captura errores sin detener el servidor
        return jsonify({"respuesta": f"Ajuste de sistema requerido: {str(e)}"})

if __name__ == "__main__":
    # Configuración dinámica de puerto para Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)