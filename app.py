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

# --- INTERFAZ INDUSTRIAL: MEDICINA, FINANZAS Y SOLANA ---
UI = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM SENTINEL PRO</title>
<style>
    body {{ background:#01080b; color:#00f2ff; font-family:'Segoe UI', sans-serif; margin:0; display:flex; height:100vh; overflow:hidden; }}
    .sidebar {{ width:320px; background:#02151c; border-right:1px solid #00f2ff33; padding:25px; display:flex; flex-direction:column; gap:15px; }}
    .main {{ flex:1; padding:30px; display:flex; flex-direction:column; background:radial-gradient(circle at center, #021a24 0%, #01080b 100%); }}
    .card {{ background:rgba(0, 242, 255, 0.05); border:1px solid #00f2ff22; padding:15px; border-radius:8px; }}
    .btn {{ background:transparent; border:1px solid #00f2ff; color:#00f2ff; padding:12px; width:100%; cursor:pointer; border-radius:4px; font-weight:bold; transition:0.3s; }}
    .btn:hover {{ background:#00f2ff; color:#000; box-shadow:0 0 15px #00f2ff; }}
    #log {{ flex:1; overflow-y:auto; background:rgba(0,0,0,0.5); padding:20px; border:1px solid #00f2ff11; font-family:monospace; font-size:13px; }}
    .usdc-box {{ border:1px dashed #27e19d; color:#27e19d; padding:15px; font-size:11px; text-align:center; margin-top:10px; word-break:break-all; }}
</style></head>
<body>
    <div class="sidebar">
        <h2 style="margin:0;">SENTINEL CORE</h2>
        <div class="card">
            <strong>FINANCIAL INTEL</strong><br><small>Hedge Fund & Market Trends</small>
            <button class="btn" onclick="quick('Análisis técnico de mercado y DeFi')">MARKET SCAN</button>
        </div>
        <div class="card">
            <strong>MEDICAL INTEL</strong><br><small>Diagnostics & Clinical Data</small>
            <button class="btn" onclick="quick('Asistencia en diagnóstico clínico avanzado')">MED SCAN</button>
        </div>
        <div class="card" style="border-color:#27e19d55;">
            <strong style="color:#27e19d;">GATEWAY SOLANA USDC</strong>
            <div class="usdc-box"><b>{Config.W_ADDR}</b></div>
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=solana:{Config.W_ADDR}" style="margin:15px auto; display:block; border:1px solid #27e19d55;">
        </div>
    </div>
    <div class="main">
        <div id="log">>> NÚCLEO SENTINEL v3.0 INICIALIZADO... CONOCIMIENTO MULTI-INDUSTRIA CARGADO.</div>
        <input type="text" id="in" style="width:100%; padding:18px; background:#000; border:1px solid #00f2ff; color:#fff; margin-top:20px;" 
               placeholder="Ingrese consulta experta..." onkeydown="if(event.key==='Enter') send()">
    </div>
    <script>
        async function send() {{
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value) return;
            const m = i.value; i.value = '';
            l.innerHTML += `<div style="color:#00f2ff88; margin-top:15px;">> CONSULTA: ${{m}}</div>`;
            const r = await fetch('/api/v1/quantum-core', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: m }})
            }});
            const d = await r.json();
            l.innerHTML += `<div style="color:#fff; padding:10px; border-left:2px solid #00f2ff;">> RESPUESTA: ${{d.response}}</div>`;
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
        # NÚCLEO DE CONOCIMIENTO TOTAL
        sys_msg = ("Eres SENTINEL CORE v3.0. Experto en Medicina clínica, Finanzas globales y Solana Blockchain. "
                  "Responde con precisión quirúrgica y nivel profesional.")
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