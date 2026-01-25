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

# --- INTERFAZ DE ALTA FIDELIDAD (MÉDICA / FINANCIERA) ---
UI = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM SENTINEL PRO</title>
<style>
    body {{ background:#020b0f; color:#00f2ff; font-family:'Segoe UI', sans-serif; margin:0; display:flex; height:100vh; }}
    .sidebar {{ width:300px; background:#04161d; border-right:1px solid #00f2ff33; padding:20px; }}
    .main {{ flex:1; padding:40px; display:flex; flex-direction:column; }}
    .card {{ background:#062029; border:1px solid #00f2ff44; padding:15px; margin-bottom:15px; border-radius:5px; }}
    .btn {{ background:transparent; border:1px solid #00f2ff; color:#00f2ff; padding:10px; width:100%; cursor:pointer; margin-top:10px; font-weight:bold; }}
    .btn:hover {{ background:#00f2ff; color:#000; }}
    #log {{ flex:1; overflow-y:auto; background:#000; padding:20px; border:1px solid #00f2ff22; font-family:monospace; font-size:13px; }}
    .usdc-box {{ border:1px dashed #27e19d; color:#27e19d; padding:10px; font-size:12px; word-break:break-all; }}
</style></head>
<body>
    <div class="sidebar">
        <h2>QUANTUM CORE</h2>
        <div class="card">
            <strong>FINANCIAL SENTINEL</strong><br><small>Hedge Fund & Crypto Analysis</small>
            <button class="btn" onclick="quick('Analyze Solana market trends')">MARKET SCAN</button>
        </div>
        <div class="card">
            <strong>MEDICAL SENTINEL</strong><br><small>Diagnostic Data Assistant</small>
            <button class="btn" onclick="quick('Analyze medical report data')">MED SCAN</button>
        </div>
        <div class="card">
            <strong>SECURE PAYMENT (USDC)</strong><br>
            <div class="usdc-box">{Config.W_ADDR}</div>
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=solana:{Config.W_ADDR}" style="margin-top:10px; width:100%;">
        </div>
    </div>
    <div class="main">
        <div id="log">>> INITIALIZING SECURE DAPP INTERFACE... READY.</div>
        <input type="text" id="in" style="width:100%; padding:15px; background:#000; border:1px solid #00f2ff; color:#fff; margin-top:20px;" 
               placeholder="Enter protocol command..." onkeydown="if(event.key==='Enter') send()">
    </div>
    <script>
        async function send() {{
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value) return;
            const m = i.value; i.value = '';
            l.innerHTML += `<div style="color:#666; margin-top:10px;">> USER: ${{m}}</div>`;
            const r = await fetch('/api/v1/quantum-core', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: m }})
            }});
            const d = await r.json();
            l.innerHTML += `<div style="color:#fff; margin-top:5px; border-left:2px solid #00f2ff; padding-left:10px;">> CORE: ${{d.response}}</div>`;
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
        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a specialized AI for High-Finance and Medicine. Provide detailed expert analysis."},
                {"role": "user", "content": msg}
            ],
            temperature=0.3
        )
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "response": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)