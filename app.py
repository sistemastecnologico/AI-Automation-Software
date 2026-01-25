import os
import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from groq import Groq

# --- CONFIGURACIÓN ENTERPRISE ---
class Config:
    W_ADDR = os.environ.get("W_ADDR", "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    MODEL_NAME = "llama-3.3-70b-versatile"
    PORT = int(os.environ.get("PORT", 10000))
    DEBUG = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - SENTINEL - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
client = Groq(api_key=Config.GROQ_API_KEY)

# --- INTERFAZ TÁCTICA DE DAPP ---
UI = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM SENTINEL v3.0</title>
<style>
    body {{ background:#050505; color:#00f2ff; font-family:'Courier New', monospace; text-align:center; padding:50px; }}
    .terminal {{ max-width:800px; margin:auto; background:#000; border:1px solid #00f2ff33; padding:20px; box-shadow:0 0 20px #00f2ff11; }}
    input {{ width:100%; padding:15px; background:#000; border:1px solid #00f2ff44; color:#fff; outline:none; }}
    #log {{ height:300px; overflow-y:auto; text-align:left; margin-bottom:20px; border-bottom:1px solid #222; padding:10px; font-size:14px; }}
</style></head>
<body>
    <div class="terminal">
        <h1>QUANTUM SENTINEL <span style="font-size:12px;">CORE_v3.0</span></h1>
        <div id="log">>> SISTEMA EN LÍNEA... EN ESPERA DE COMANDO TÉCNICO.</div>
        <input type="text" id="in" placeholder="Query (Finance, Medical, Web3)..." onkeydown="if(event.key==='Enter') send()">
    </div>
    <script>
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
            l.innerHTML += `<div style="color:#fff;">> CORE: ${{d.response}}</div>`;
            if(d.blockchain_gateway) {{
                l.innerHTML += `<div><img src="${{d.blockchain_gateway.qr}}" style="width:150px; margin-top:10px; border:1px solid #00f2ff;"></div>`;
            }}
            l.scrollTop = l.scrollHeight;
        }}
    </script>
</body></html>
"""

@app.route("/")
def index(): 
    return Response(UI, mimetype='text/html')

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.json
        msg = data.get("message", "").strip()
        if not msg or len(msg) > 1500:
            return jsonify({"status": "error", "response": "Safety limit exceeded."}), 400

        sys_prompt = ("You are QUANTUM CORE v3.0. Expert in Solana DApps, Finance, and Medicine. "
                      "Provide technical, precise answers in the user's language.")

        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": msg}],
            temperature=0.2
        )

        res_text = comp.choices[0].message.content
        out = {"response": res_text}

        if any(x in msg.lower() for x in ["pago", "pay", "solana", "hire", "medical"]):
            out["blockchain_gateway"] = {
                "qr": f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=solana:{Config.W_ADDR}"
            }
        return jsonify(out)
    except Exception as e:
        return jsonify({"status": "error", "response": f"Protocol Breach: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)