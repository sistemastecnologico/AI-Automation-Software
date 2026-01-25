import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from groq import Groq

class Config:
    # Asegúrate de que esta sea tu wallet correcta
    W_ADDR = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    MODEL_NAME = "llama-3.3-70b-versatile"
    PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)
CORS(app)
client = Groq(api_key=Config.GROQ_API_KEY)

UI = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM PRIME | US INSTITUTIONAL</title>
<style>
    :root {{ --blue: #007aff; --bg: #050505; --card: #0d0d0d; --border: #1a1a1a; }}
    body {{ background: var(--bg); color: white; font-family: 'Inter', sans-serif; margin:0; display:flex; height:100vh; overflow:hidden; }}
    .sidebar {{ width:380px; background:#000; border-right:1px solid var(--border); padding:40px; display:flex; flex-direction:column; }}
    .main {{ flex:1; padding:60px; background: radial-gradient(circle at top right, #001f3f 0%, #050505 70%); display:flex; flex-direction:column; }}
    .card {{ background:var(--card); border:1px solid var(--border); padding:20px; border-radius:12px; margin-bottom:20px; }}
    .btn {{ background:var(--blue); color:white; border:none; padding:15px; width:100%; border-radius:8px; font-weight:bold; cursor:pointer; text-transform:uppercase; font-size:11px; }}
    /* ESTILO PARA EL BOTÓN DE PAGO REPARADO */
    .pay-link {{ display: block; text-decoration: none; background: transparent; border: 1px solid #00ffa3; color: #00ffa3; padding: 15px; border-radius: 8px; font-weight: bold; text-align: center; margin-top: 15px; transition: 0.3s; }}
    .pay-link:hover {{ background: #00ffa3; color: black; box-shadow: 0 0 20px #00ffa3; }}
    #log {{ flex:1; overflow-y:auto; background:rgba(0,0,0,0.5); padding:30px; border-radius:12px; border: 1px solid var(--border); font-family:'SF Mono', monospace; font-size:14px; line-height:1.6; color:#d0d0d0; }}
    input {{ width:100%; padding:20px; background:#000; border:1px solid var(--border); color:white; border-radius:12px; font-size:16px; margin-top:20px; outline:none; }}
    .disclaimer {{ color:#ff453a; font-size:10px; margin-bottom:15px; text-align:center; padding:10px; border:1px dashed #ff453a44; border-radius:8px; }}
</style></head>
<body>
    <div class="sidebar">
        <h2 style="color:var(--blue); letter-spacing:5px;">QUANTUM</h2>
        <div class="card">
            <strong>FINANCIAL ENGINE</strong>
            <button class="btn" onclick="ask('Analyze SOL/USDC market efficiency')">Execute Analysis</button>
        </div>
        <div class="card">
            <strong>MEDICAL ENGINE</strong>
            <button class="btn" onclick="ask('Evaluate longevity bio-protocols')">Execute Diagnostics</button>
        </div>
        <div style="margin-top:auto; text-align:center;">
            <div style="background:white; padding:10px; border-radius:8px; width:150px; margin:0 auto 15px;">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=solana:{Config.W_ADDR}" style="width:100%">
            </div>
            <a href="solana:{Config.W_ADDR}" class="pay-link">TRUST WALLET / PHANTOM</a>
            <code style="font-size:9px; color:#444; margin-top:10px; display:block;">{Config.W_ADDR}</code>
        </div>
    </div>
    <div class="main">
        <div class="disclaimer">
            NOTICE: AI outputs are for advisory purposes only. Systems may hallucinate or produce errors. Verify with a human professional.
        </div>
        <div id="log">>> INITIALIZING QUANTUM CORE... <br>>> STANDBY FOR ELITE COMMANDS.</div>
        <input type="text" id="in" placeholder="Command Input..." onkeydown="if(event.key==='Enter') send()">
    </div>
    <script>
        async function send() {{
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value) return;
            const m = i.value; i.value = '';
            l.innerHTML += `<div style="color:var(--blue); margin-top:20px;">> CMD: ${{m}}</div>`;
            const r = await fetch('/api/v1/quantum-core', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: m }})
            }});
            const d = await r.json();
            l.innerHTML += `<div style="color:#eee; padding:15px 0; border-left:1px solid var(--blue); padding-left:15px;">> RESULT: ${{d.response}}</div>`;
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
        # PROMPT POTENCIADO PARA HABLAR COMO UN BILLONARIO GENIO
        sys_msg = (
            "You are QUANTUM PRIME, an ultra-elite AI consultant for US Billionaires and VC Founders. "
            "You speak with authority, precision, and absolute technical mastery in Finance, Medicine, and Web3. "
            "Your tone is professional yet disruptive. "
            "IMPORTANT: Always acknowledge that as an AI, you are capable of errors and require human validation. "
            "Respond in the same language as the user (English or Spanish)."
        )
        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": msg}],
            temperature=0.3
        )
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "response": "Core error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)