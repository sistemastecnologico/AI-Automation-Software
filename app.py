import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from groq import Groq

class Config:
    W_ADDR = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    MODEL_NAME = "llama-3.3-70b-versatile"
    PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)
CORS(app)
client = Groq(api_key=Config.GROQ_API_KEY)

# HTML separado para evitar errores de sintaxis en Python
UI_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM PRIME | US Elite</title>
<style>
    body { background: #050505; color: white; font-family: 'Inter', sans-serif; margin:0; display:flex; height:100vh; overflow:hidden; }
    .sidebar { width:350px; background:#000; border-right:1px solid #1a1a1a; padding:40px; display:flex; flex-direction:column; }
    .main { flex:1; padding:60px; background: radial-gradient(circle at top right, #001a33 0%, #050505 80%); display:flex; flex-direction:column; }
    .header { font-size:10px; letter-spacing:4px; color:#007aff; font-weight:800; margin-bottom:40px; text-transform:uppercase; }
    .card { background:#0d0d0d; border:1px solid #1a1a1a; padding:20px; border-radius:12px; margin-bottom:20px; }
    .btn { background:#007aff; color:white; border:none; padding:15px; width:100%; border-radius:8px; font-weight:700; cursor:pointer; text-transform:uppercase; font-size:11px; }
    /* BOTÓN DE PAGO SOLANA USDC SPL */
    .pay-link { display:block; text-decoration:none; background:transparent; border:1px solid #00ffa3; color:#00ffa3; padding:16px; border-radius:8px; font-weight:800; text-align:center; margin-top:20px; font-size:12px; transition: 0.3s; }
    .pay-link:hover { background:#00ffa3; color:black; box-shadow:0 0 20px #00ffa3; }
    #log { flex:1; overflow-y:auto; background:rgba(0,0,0,0.4); padding:30px; border-radius:12px; border: 1px solid #1a1a1a; font-family:monospace; color:#888; }
    input { width:100%; padding:22px; background:#000; border:1px solid #1a1a1a; color:white; border-radius:12px; font-size:16px; margin-top:30px; outline:none; }
</style></head>
<body>
    <div class="sidebar">
        <div class="header">Quantum Elite Terminal</div>
        <div class="card">
            <strong style="color:#007aff">FINANCIAL ARCHITECT</strong>
            <p style="font-size:11px; color:#444;">Institutional-grade DeFi & SaaS scaling.</p>
            <button class="btn" onclick="ask('Analyze SOL institutional liquidity')">Run Analysis</button>
        </div>
        <div style="margin-top:auto; text-align:center;">
            <div style="background:white; padding:10px; border-radius:10px; width:140px; margin:0 auto 20px;">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=140x140&data=solana:FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp" style="width:100%">
            </div>
            <a href="solana:FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp?label=Quantum_Prime_Service&message=USDC_SPL_Consulting_Fee" class="pay-link">PAY WITH USDC (SOLANA SPL)</a>
        </div>
    </div>
    <div class="main">
        <div id="log">>> QUANTUM CORE v5.0 ACTIVE... <br>>> INSTITUTIONAL PORTAL CONNECTED.</div>
        <input type="text" id="in" placeholder="Enter High-Level Commands..." onkeydown="if(event.key==='Enter') send()">
    </div>
    <script>
        async function send() {
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value) return;
            const m = i.value; i.value = '';
            l.innerHTML += '<div style="color:#007aff; margin-top:20px; font-weight:bold;">> COMMAND: ' + m + '</div>';
            const r = await fetch('/api/v1/quantum-core', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: m })
            });
            const d = await r.json();
            l.innerHTML += '<div style="color:#eee; padding:10px 0; border-left:2px solid #007aff; padding-left:15px;">> ANALYSIS: ' + d.response + '</div>';
            l.scrollTop = l.scrollHeight;
        }
        function ask(t) { document.getElementById('in').value = t; send(); }
    </script>
</body></html>
"""

@app.route("/")
def index(): return Response(UI_HTML, mimetype='text/html')

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.json
        msg = data.get("message", "").strip()
        sys_msg = "You are QUANTUM PRIME, an elite AI advisor for US Billionaires. Expert in Software and Finance. Professional and direct."
        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": msg}],
            temperature=0.2
        )
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "response": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)