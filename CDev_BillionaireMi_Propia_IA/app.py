import os
from flask import Flask, render_template, request, jsonify, session
from groq import Groq

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "billonario_key_2026")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    return render_template("dashboard.html", user=session.get('user'))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        mensaje = request.json.get("mensaje", "").lower()
        if "grafico" in mensaje:
            config = "{type:'bar',data:{labels:['Ene','Feb','Mar'],datasets:[{label:'Ganancias',data:[400,900,2400]}]}}"
            chart_url = f"https://quickchart.io/chart?c={config}".replace(" ", "")
            respuesta_ia = f"💹 **Análisis**: <br><img src='{chart_url}' width='100%'>"
        elif "crea" in mensaje:
            prompt = mensaje.replace("crea", "").strip().replace(" ", "%20")
            img_url = f"https://pollinations.ai/p/{prompt}?width=512&height=512"
            respuesta_ia = f"🎨 **IA**: <br><img src='{img_url}' width='100%' style='border-radius:10px;'>"
        else:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": mensaje}]
            )
            respuesta_ia = completion.choices[0].message.content
        return jsonify({"respuesta": respuesta_ia})
    except Exception as e:
        return jsonify({"respuesta": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)