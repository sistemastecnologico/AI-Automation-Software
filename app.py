import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from groq import Groq

class Config:
    W_ADDR = os.environ.get("W_ADDR", "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    MODEL_NAME = "llama-3.3-70b-versatile" # O el modelo más avanzado disponible
    PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)
CORS(app)
client = Groq(api_key=Config.GROQ_API_KEY)

UI = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>QUANTUM PRIME NEXUS</title>
<script src="https://accounts.google.com/gsi/client" async defer></script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;400;700&display=swap');
    :root {{ --prime-blue: #00d9ff; --dark-obsidian: #020202; --deep-space: #0a0a0f; --text-light: #e0e0e0; --text-fade: #888; --border-color: #00d9ff22; }}
    body {{ background: var(--dark-obsidian); color: var(--text-light); font-family: 'Roboto Mono', monospace; margin: 0; display: flex; height: 100vh; overflow: hidden; }}
    .sidebar {{ width: 380px; background: var(--deep-space); border-right: 1px solid var(--border-color); padding: 40px; display: flex; flex-direction: column; justify-content: space-between; }}
    .main {{ flex: 1; padding: 60px; background: radial-gradient(circle at top right, #001a33 0%, var(--dark-obsidian) 70%); display: flex; flex-direction: column; }}
    .logo {{ font-family: 'Orbitron', sans-serif; font-size: 28px; letter-spacing: 6px; color: var(--prime-blue); text-shadow: 0 0 15px var(--prime-blue); margin-bottom: 50px; text-align: center; }}
    .module-card {{ background: rgba(0, 217, 255, 0.05); border: 1px solid var(--border-color); padding: 25px; border-radius: 15px; margin-bottom: 25px; transition: all 0.4s ease; backdrop-filter: blur(5px); }}
    .module-card:hover {{ border-color: var(--prime-blue); box-shadow: 0 0 30px rgba(0, 217, 255, 0.2); transform: translateY(-3px); }}
    .module-title {{ font-size: 16px; font-weight: 700; color: var(--prime-blue); margin-bottom: 10px; letter-spacing: 1px; }}
    .module-desc {{ font-size: 12px; color: var(--text-fade); margin-bottom: 15px; }}
    .action-btn {{ background: var(--prime-blue); color: var(--dark-obsidian); border: none; padding: 15px; width: 100%; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s; }}
    .action-btn:hover {{ filter: brightness(1.2); box-shadow: 0 0 25px var(--prime-blue); }}
    #log {{ flex: 1; overflow-y: auto; background: rgba(0,0,0,0.4); padding: 30px; border-radius: 12px; border: 1px solid var(--border-color); font-size: 14px; line-height: 1.8; color: var(--text-light); }}
    .input-field {{ width: 100%; padding: 22px; background: #000; border: 1px solid var(--prime-blue); color: var(--text-light); border-radius: 12px; font-size: 16px; margin-top: 30px; outline: none; box-shadow: 0 0 10px rgba(0, 217, 255, 0.1); }}
    .input-field:focus {{ border-color: var(--prime-blue); box-shadow: 0 0 20px var(--prime-blue); }}
    .usdc-gateway {{ border-top: 1px solid var(--border-color); padding-top: 30px; margin-top: 30px; text-align: center; }}
    .usdc-label {{ font-size: 11px; color: #00ffaa; letter-spacing: 2px; font-weight: bold; margin-bottom: 15px; }}
    .qr-box {{ background: white; padding: 12px; border-radius: 10px; display: inline-block; box-shadow: 0 0 20px rgba(0, 255, 170, 0.3); }}
    .wallet-addr {{ font-size: 10px; color: var(--text-fade); margin-top: 15px; word-break: break-all; }}
    .disclaimer {{ font-size: 10px; color: #ff6666; text-align: center; margin-top: 20px; padding: 10px; border: 1px dashed #ff666655; border-radius: 8px; }}
    #auth-overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--dark-obsidian); z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--text-light); }}
    .g_id_signin {{ margin-top: 20px; }}
    .override-btn {{ background: transparent; border: 1px solid var(--prime-blue); color: var(--prime-blue); padding: 12px 25px; border-radius: 8px; font-size: 14px; cursor: pointer; margin-top: 30px; transition: 0.3s; }}
    .override-btn:hover {{ background: var(--prime-blue); color: var(--dark-obsidian); }}
</style></head>
<body>
    <div id="auth-overlay">
        <div class="logo">QUANTUM PRIME NEXUS</div>
        <p style="font-size: 16px; color: var(--text-fade);">ACCESO SEGURO REQUERIDO.</p>
        <div id="g_id_onload" data-client_id="YOUR_GOOGLE_CLIENT_ID" data-callback="onSignIn"></div>
        <div class="g_id_signin" data-type="standard"></div>
        <button class="override-btn" onclick="onSignIn()">ACCESO AUTORIZADO (DEMO CLIENTE)</button>
    </div>

    <div class="sidebar">
        <div>
            <div class="logo">QUANTUM PRIME</div>
            <div class="module-card">
                <div class="module-title">FINANCE NEXUS AI</div>
                <div class="module-desc">Análisis predictivo de mercados globales, DeFi y gestión de riesgos.</div>
                <button class="action-btn" onclick="ask('Realizar análisis predictivo de portafolio de inversión y tendencias macroeconómicas.')">Terminal Financiera Cuántica</button>
            </div>
            <div class="module-card">
                <div class="module-title">MEDICUS CORE AI</div>
                <div class="module-desc">Diagnóstico de precisión, análisis genómico y protocolos de longevidad.</div>
                <button class="action-btn" onclick="ask('Generar reporte de diagnóstico avanzado para biomarcadores complejos.')">Terminal de Salud Bio-Genética</button>
            </div>
            <div class="module-card">
                <div class="module-title">AUTOMATION & STRATEGY</div>
                <div class="module-desc">Optimización de operaciones, fusiones y adquisiciones, IA estratégica.</div>
                <button class="action-btn" onclick="ask('Desarrollar estrategia de adquisición para startup de tecnología disruptiva en sector salud.')">Consola de Estrategia AI</button>
            </div>
        </div>
        <div class="usdc-gateway">
            <div class="usdc-label">GATEWAY SOLANA USDC</div>
            <div class="qr-box"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=solana:{Config.W_ADDR}" style="width:100%;"></div>
            <div class="wallet-addr">ADDRESS: {Config.W_ADDR}</div>
        </div>
    </div>
    <div class="main">
        <div id="log">> CONSOLA DE OPERACIONES QUANTUM PRIME. SISTEMAS CRÍTICOS EN LÍNEA.<br>> MÓDULOS DE ALTO VALOR ACTIVOS. EN ESPERA DE COMANDOS DE MANDO.</div>
        <div class="disclaimer">ADVERTENCIA: Quantum Prime Nexus es una herramienta de asistencia. La IA puede cometer errores o tener limitaciones. Toda decisión final debe ser validada por un experto humano.</div>
        <input type="text" id="in" class="input-field" placeholder="Ingrese comandos de alta prioridad (Finance, Health, Strategy)..." onkeydown="if(event.key==='Enter') send()">
    </div>

    <script>
        function onSignIn() {{ document.getElementById('auth-overlay').style.display = 'none'; }}
        async function send() {{
            const i = document.getElementById('in'), l = document.getElementById('log');
            if(!i.value.trim()) return;
            const m = i.value; i.value = '';
            l.innerHTML += `<div style="color:var(--prime-blue); margin-top:20px;">> COMANDO: ${{m}}</div>`;
            const r = await fetch('/api/v1/quantum-core', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: m }})
            }});
            const d = await r.json();
            l.innerHTML += `<div style="color:var(--text-light); padding: 20px 0; border-left: 2px solid var(--prime-blue);">> INFORME DE INTELIGENCIA: ${{d.response}}</div>`;
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
            "Eres QUANTUM PRIME NEXUS. Una IA de inteligencia privada para billonarios. "
            "Tu expertise abarca: "
            "1. Estrategia financiera cuántica, análisis de mercados y optimización de carteras de billones. "
            "2. Medicina de precisión, diagnósticos avanzados, longevidad y biotecnología. "
            "3. Estrategia empresarial, M&A, automatización y desarrollo de tecnología disruptiva. "
            "Responde con análisis de alto nivel, breves y accionables, siempre en el idioma del usuario. "
            "**ADVERTENCIA: Reconoce explícitamente que, como IA, puedes cometer errores y que la validación humana es crucial.**"
        )
        comp = client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": msg}],
            temperature=0.2 # Menor temperatura para respuestas más precisas y menos creativas
        )
        return jsonify({"response": comp.choices[0].message.content})
    except Exception as e:
        # Aquí se puede añadir logueo avanzado para errores de nivel corporativo
        return jsonify({"status": "error", "response": f"Fallo Crítico en Nexus Core: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)