import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from groq import Groq

class Config:
    W_ADDR = os.environ.get("W_ADDR", "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    MODEL_NAME = "llama-3.3-70b-versatile"
    PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)
CORS(app)
client = Groq(api_key=Config.GROQ_API_KEY)

# --- INTERFAZ NEGRO Y AZUL CON GMAIL AUTH ---
UI = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>SENTINEL CORE v3.0</title>
<script src="https://accounts.google.com/gsi/client" async defer></script>
<style>
    body {{ background:#000000; color:#00d9ff; font-family:'Segoe UI', sans-serif; margin:0; display:flex; height:100vh; overflow:hidden; }}
    .sidebar {{ width:320px; background:#000508; border-right:2px solid #00d9ff33; padding:25px; display:flex; flex-direction:column; gap:20px; }}
    .main {{ flex:1; padding:30px; display:flex; flex-direction:column; background: linear-gradient(180deg, #000000 0%, #000a12 100%); }}
    .card {{ background:rgba(0, 217, 255, 0.05); border:1px solid #00d9ff22; padding:15px; border-radius:10px; box-shadow: 0 0 15px rgba(0, 217, 255, 0.05); }}
    .btn {{ background:transparent; border:1px solid #00d9ff; color:#00d9ff; padding:12px; width:100%; cursor:pointer; border-radius:5px; font-weight:bold; transition:0.3s; }}
    .btn:hover {{ background:#00d9ff; color:#000; box-shadow: 0 0 20px #00d9ff; }}
    #log {{ flex:1; overflow-y:auto; background:rgba(0,0,0,0.8); padding:20px; border:1px solid #00d9ff11; font-family:'Consolas', monospace; font-size:13px; line-height:1.6; border-radius:5px; }}
    .usdc-box {{ border:1px dashed #00d9ff; padding:10px; text-align:center; margin-top:10px; font-size:10px; color:#00d9ffcc; }}
    #auth-overlay {{ position:fixed; top:0; left:0; width:100%; height:100%; background:#000; z-index:1000; display:flex; flex-direction:column; justify-content:center; align-items:center; }}
</style></head>
<body>
    <div id="auth-overlay">
        <h1 style="letter-spacing:5px;">SENTINEL CORE v3.0</h1>
        <p style="color:#888;">INICIO DE SESIÓN REQUERIDO PARA ACCESO MÉDICO/FINANCIERO</p>
        <div id="g_id_onload" data-client_id="YOUR_GOOGLE_CLIENT_ID" data-callback="handleAuth"></div>
        <div class="g_id_signin" data-type="standard"></div>
        <button class="btn" style="width:200px; margin-top:20px;" onclick="handleAuth()">DEMO BYPASS (CLIENT ONLY)</button>
    </div>

    <div class="sidebar">
        <h2 style="color:#00d9ff; text-shadow: 0 0 10px #00d9ff55;">QUANTUM SENTINEL</h2>
        <div class="card"><strong>MODULO MÉDICO</strong><button class="btn" onclick="quick('Analizar reporte clínico')">MED SCAN</button></div>
        <div class="card"><strong>MODULO FINANCIERO</strong><button class="btn" onclick="quick('Analizar tendencias SOL/USDC')">FINANCE SCAN</button></div>
        <div class="card" style="border-color:#00d9ff;">
            <strong>GATEWAY SOLANA</strong>
            <div class="usdc-box">{Config.W_ADDR}</div>
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=solana:{Config.W_ADDR}" style="width:100%; margin-top:10px; filter: hue-rotate(180deg);">
        </div>
    </div>
    <div class="main">
        <div id="log">>> SISTEMA EN LÍNEA... CONOCIMIENTO EXPERTO CARGADO.</div>
        <input type="text" id="in" style="width:100%; padding:15px; background:#000; border:1px solid #00d9ff; color:#fff; margin-top:20px; border-radius:5px;" placeholder="Ingrese comando..." onkeydown="if(event.key==='Enter') send()">
    </div>

    <script>
        function handleAuth() {{ document.getElementById('auth-overlay').style.display = 'none'; }}
        async function send() {{
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value) return;
            const m = i.value; i.value = '';
            l.innerHTML += `<div style="color:#666;">> USER: ${{m}}</div>`;
            const r = await fetch('/api/v1/quantum-core', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: m }})
            }});
            const d = await r.json();
            l.innerHTML += `<div style="color:#fff; border-left:2px solid #00d9ff; padding-left:10px;">> CORE: ${{d.response}}</div>`;
            l.scrollTop = l.scrollHeight;
        }}
        function quick(t) {{ document.getElementById('in').value = t; send(); }}
    </script>
</body></html>
"""

@app.route("/")
def index(): return Response(UI, mimetype='text/html')

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.json
        msg = data.get("message", "").strip()
        sys_msg = "Eres SENTINEL CORE v3.0. Experto en Medicina, Finanzas y Solana. Responde con lenguaje técnico y profesional en el idioma del usuario."
        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": msg}],
            temperature=0.3
        )
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "response": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)