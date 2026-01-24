import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    # Carga el diseño original con Dashboard y Donaciones
    return render_template("dashboard.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        mensaje = data.get("mensaje", "").lower()
        
        # FILTRO DE SEGURIDAD Y LEGALIDAD (Anti-morbo / No humanos)
        if any(palabra in mensaje for palabra in ["imagen", "genera", "crea"]):
            # Forzamos que la IA solo genere cosas útiles y legales
            prompt_legal = (f"{mensaje} - photorealistic, professional business asset, "
                           "no humans, no people, no NSFW, legal and clean content, billionaire style")
            
            url_imagen = f"https://pollinations.ai/p/{prompt_legal.replace(' ', '_')}?width=1080&height=720&seed=99&model=flux"
            
            return jsonify({
                "respuesta": "Generando activo visual legal para tu imperio...",
                "imagen": url_imagen
            })

        # IA DE ESTRATEGIA (GROQ)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": mensaje}]
        )
        return jsonify({"respuesta": completion.choices[0].message.content})
        
    except Exception as e:
        return jsonify({"respuesta": f"Error de sistema: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)