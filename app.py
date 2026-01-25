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

# --- INTERFAZ ELITE: SOFTWARE & FINANCE ---
UI = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM PRIME | US Institutional</title>
<style>
    :root {{ --blue: #007aff; --bg: #050505; --card: #0d0d0d; --border: #1a1a1a; }}
    body {{ background: var(--bg); color: white; font-family: 'Inter', sans-serif; margin:0; display:flex; height:100vh; overflow:hidden; }}
    .sidebar {{ width:380px; background:#000; border-right:1px solid var(--border); padding:40px; display:flex; flex-direction:column; }}
    .main {{ flex:1; padding:60px; background: radial-gradient(circle at top right, #001a33 0%, #050505 80%); display:flex; flex-direction:column; }}
    .header {{ font-size:10px; letter-spacing:4px; color:var(--blue); font-weight:800; margin-bottom:40px; text-transform:uppercase; }}
    .card {{ background:var(--card); border:1px solid var(--border); padding:20px; border-radius:12px; margin-bottom:20px; transition:0.3s; }}
    .card:hover {{ border-color:var(--blue); box-shadow: 0 0 25px rgba(0,122,255,0.1); }}
    .btn {{ background:var(--blue); color:white; border:none; padding:15px; width:100%; border-radius:8px; font-weight:700; cursor:pointer; text-transform:uppercase; font-size:11px; }}
    /* BOTÓN DE PAGO REPARADO - USDC SOLANA SPL */
    .pay-btn {{ display:block; text-decoration:none; background:transparent; border:1px solid #00ffa3; color:#00ffa3; padding:16px; border-radius:8px; font-weight:800; text-align:center; margin-top:20px; transition:0.3s; font-size:12px; }}
    .pay-btn:hover {{ background:#00ffa3; color:black; box-shadow:0 0 20px #00ffa3; }}
    #log {{ flex:1; overflow-y:auto; background:rgba(0,0,0,0.4); padding:30px; border-radius:12px; border: 1px solid var(--border); font-family:'SF Mono', monospace; font-size:14px; line-height:1.8; color:#999; }}
    input {{ width:100%; padding:22px; background:#000; border:1px solid var(--border); color:white; border-radius:12px; font-size:16px; margin-top:30px; outline:none; }}
    .disclaimer {{ color:#ff453a; font-size:10px; margin-bottom:20px; text-align:center; padding:10px; border:1px dashed #ff453a33; border-radius:8px; }}
</style></head>
<body>
    <div class="sidebar">
        <div class="header">System Status: Elite Access</div>
        <div class="card">
            <strong style="color:var(--blue)">FINANCIAL SOFTWARE ARCHITECT</strong>
            <p style="font-size:12px; color:#555; margin-top:5px;">Sistemas DeFi de grado institucional y escalado de capital.</p>
            <button class="btn" onclick="ask('Analiza la liquidez de SOL y el impacto en el mercado institucional de EE. UU.')">Run Analysis</button>
        </div>
        <div class="card">
            <strong style="color:var(--blue)">AI INFRASTRUCTURE</strong>
            <p style="font-size:12px; color:#555; margin-top:5px;">Soluciones de LLM personalizadas para tareas de alta frecuencia.</p>
            <button class="btn" onclick="ask('Escala un framework de IA para una plataforma SaaS con 10M de usuarios')">Deploy Core</button>
        </div>
        <div style="margin-top:auto; text-align:center;">
            <div style="background:white; padding:10px; border-radius:10px; width:150px; margin:0 auto 20px;">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=solana:{Config.W_ADDR}" style="width:100%">
            </div>
            <a href="solana:{Config.W_ADDR}?label=Quantum_Prime_Elite&message=USDC_SPL_Payment" class="pay-btn">PAY WITH USDC (SOLANA SPL)</a>
        </div>
    </div>
    <div class="main">
        <div class="disclaimer">
            NOTICE: Quantum Prime es una IA de alto nivel. Validación humana obligatoria para activos financieros y software corporativo.
        </div>
        <div id="log">>> QUANTUM CORE v5.0 ACTIVE... <br>>> INSTITUTIONAL PORTAL CONNECTED.</div>
        <input type="text" id="in" placeholder="Enter High-Level Commands..." onkeydown="if(event.key==='Enter') send()">
    </div>
    <script>
        async function send() {{
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value) return;
            const m = i.value; i.value = '';
            l.innerHTML += `<div style="color:var(--blue); margin-top:20px; font-weight:bold;">> COMMAND: ${{m}}</div>`;
            const r = await fetch('/api/v1/quantum-core', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: m }})
            }});
            const d = await r.json();
            l.innerHTML += `<div style="color:#eee; padding:20px 0; border-left:2px solid var(--blue); padding-left:15px;">> ANALYSIS: ${{d.response}}</div>`;
            l.scrollTop = l.scrollHeight;
        }}
        function ask(t) {{ document.getElementById('in').value = t; send(); }}
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
        sys_msg = (
            "Eres QUANTUM PRIME, una IA de élite para inversores billonarios de EE. UU. "
            "Experto en arquitectura de Software, Finanzas y Web3. "
            "Responde con autoridad técnica. Siempre admite que puedes cometer errores para generar confianza."
        )
        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": msg}],
            temperature=0.2
        )
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "response": "Error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)