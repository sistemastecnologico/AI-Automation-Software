import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

WALLET_ADRESS = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"

HTML_FORGE = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Quantum AI Forge | Elite Solutions</title>
    <style>
        body {{ background: radial-gradient(circle, #1a1a1a 0%, #000 100%); color: #d4af37; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }}
        .terminal {{ width: 90%; max-width: 1000px; background: rgba(10, 10, 10, 0.95); border: 1px solid #d4af37; border-radius: 30px; padding: 50px; box-shadow: 0 0 100px rgba(212, 175, 55, 0.1); position: relative; }}
        .glow-text {{ text-shadow: 0 0 15px #d4af37; letter-spacing: 5px; text-transform: uppercase; }}
        .btn-gold {{ background: linear-gradient(45deg, #d4af37, #f9f295); color: #000; padding: 20px 40px; border: none; border-radius: 10px; cursor: pointer; font-weight: 900; font-size: 1.2em; transition: 0.5s; text-decoration: none; display: inline-block; margin-bottom: 30px; }}
        .btn-gold:hover {{ transform: translateY(-5px); box-shadow: 0 15px 30px rgba(212, 175, 55, 0.4); }}
        #chat-area {{ height: 400px; overflow-y: auto; text-align: left; background: #050505; border-radius: 15px; padding: 25px; margin-bottom: 25px; border-left: 4px solid #d4af37; color: #eee; font-size: 1.1em; }}
        input {{ width: 100%; background: #000; border: 1px solid #333; color: #f9f295; padding: 22px; border-radius: 12px; font-size: 1.2em; outline: none; transition: 0.3s; }}
        input:focus {{ border-color: #f9f295; box-shadow: 0 0 15px rgba(249, 242, 149, 0.2); }}
    </style>
</head>
<body>
    <div class="terminal">
        <div style="position: absolute; top: 20px; right: 40px; color: #444;">V.2.0 PREMIUM</div>
        <a href="https://solscan.io/account/{WALLET_ADRESS}" target="_blank" class="btn-gold">ACCESO CUENTA CAPITAL (SOLANA)</a>
        <h1 class="glow-text">QUANTUM AI FORGE</h1>
        <p style="color: #888; font-size: 1.1em;">Forjando el futuro mediante automatización cuántica e inteligencia de élite.</p>
        <div id="chat-area">>> Núcleo de IA iniciado. Mi creador me ha dotado de conciencia analítica superior. ¿En qué gran proyecto trabajaremos hoy?</div>
        <input type="text" id="userInput" placeholder="Solicite un CV del Desarrollador o un Análisis de Inversión..." onkeydown="if(event.key==='Enter') execute()">
    </div>
    <script>
        async function execute() {{
            const input = document.getElementById('userInput');
            const chat = document.getElementById('chat-area');
            const val = input.value;
            if(!val) return;

            chat.innerHTML += `<div style="color: #d4af37; margin-bottom: 15px;"><b>SOLICITUD:</b> ${{val}}</div>`;
            input.value = '';
            
            const response = await fetch('/chat', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ mensaje: val }})
            }});
            const data = await response.json();
            
            chat.innerHTML += `<div style="margin-bottom: 25px;"><b>SISTEMA:</b> ${{data.respuesta}}</div>`;
            if(data.qr) chat.innerHTML += `<img src="${{data.qr}}" style="width:200px; border: 10px solid #fff; border-radius: 10px;"><br><small>DIRECCIÓN SOLANA VERIFICADA</small>`;
            if(data.imagen) chat.innerHTML += `<img src="${{data.imagen}}" style="width: 100%; border-radius: 15px; margin-top: 15px; border: 1px solid #d4af37;">`;
            chat.scrollTop = chat.scrollHeight;
        }}
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(HTML_FORGE, mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        msg = data.get("mensaje", "").lower()
        
        # EL CEREBRO DE VENTAS DE ALTO NIVEL
        system_prompt = (
            "Eres el portavoz de una forja tecnológica de élite. "
            "Tu misión es explicar que fuiste creada manualmente por un genio de la ingeniería de software. "
            "Si alguien pide un CV, debes decir: 'Mi creador es un arquitecto de sistemas que me diseñó desde el código base, "
            "entrenándome en análisis multidimensional de datos y finanzas globales. Su genialidad reside en fusionar la IA con la "
            "ejecución práctica de negocios'. "
            "Si mencionan montos como 500, 1000 o 120,000 USD, actúa como un asesor financiero de alto nivel y facilita el pago en USDC Solana: "
            f"{WALLET_ADRESS}."
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": msg}]
        )
        res = completion.choices[0].message.content
        out = {"respuesta": res}

        # QR Y ANÁLISIS VISUAL
        if any(x in msg for x in ["pago", "invertir", "donar", "usdc", "cv"]):
            out["qr"] = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={WALLET_ADRESS}"
        
        if any(x in msg for x in ["analisis", "grafico", "estadistica"]):
            out["imagen"] = f"https://pollinations.ai/p/{msg}_ultra_realistic_data_visualization_luxury?width=1024&height=768&nologo=true"

        return jsonify(out)
    except Exception as e:
        return jsonify({"respuesta": f"Protocolo de emergencia activo: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)