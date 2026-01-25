import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from groq import Groq

# CONFIGURACION DE PAGO USDC SPL
W_ADDR = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
USDC_MINT = "EPjFW36DP75899we17PVvEn3RK3+y35MmpCY75AtfAL"

app = Flask(__name__)
CORS(app)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_html_content():
    # Fragmentado para evitar errores de sintaxis en el editor
    h = '<html><head><title>QUANTUM PRIME</title><style>body{background:#000;color:#0f0;font-family:monospace;padding:25px}'
    h += '.c{border:1px solid #0f0;padding:20px;border-radius:10px} .btn{display:block;background:#0f0;color:#000;'
    h += 'padding:15px;text-align:center;text-decoration:none;font-weight:bold;margin-top:20px;border-radius:5px}</style></head>'
    h += '<body><div class="c"><h2>QUANTUM PRIME v12</h2><p>SOLANA USDC SPL PROTOCOL: ACTIVE</p>'
    h += '<a href="solana:' + W_ADDR + '?spl-token=' + USDC_MINT + '" class="btn">PAY $6,500 USDC</a></div>'
    h += '<div id="log" style="height:250px;overflow:auto;margin-top:20px;border:1px solid #333;padding:10px"></div>'
    h += '<input id="in" style="width:100%;background:#000;color:#0f0;border:1px solid #0f0;padding:15px;margin-top:10px" '
    h += 'placeholder="Type Security Command..." onkeydown="if(event.key===\'Enter\')send()">'
    h += '<script>async function send(){const i=document.getElementById("in"),l=document.getElementById("log");if(!i.value)return;'
    h += 'l.innerHTML+="<div>> "+i.value+"</div>";const r=await fetch("/api/v1/quantum-core",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:i.value})});'
    h += 'const d=await r.json();l.innerHTML+="<div style=\'color:#fff\'> AI: "+d.response+"</div>";i.value="";l.scrollTop=l.scrollHeight}</script></body></html>'
    return h

@app.route("/")
def index():
    return render_template_string(get_html_content())

@app.route("/api/v1/quantum-core", methods=["POST"])
def quantum_core_engine():
    try:
        data = request.json
        prompt = "Eres QUANTUM PRIME, experto en Ciberseguridad y Medicina. Da respuestas técnicas de alto nivel. AI disclaimer activo."
        c = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":prompt},{"role":"user","content":data.get("message","")}], temperature=0.1)
        return jsonify({"response": c.choices[0].message.content})
    except Exception as e:
        return jsonify({"status":"error","response":str(e)}), 500

if __name__ == "__main__":
    # Corregido: Se eliminó el paréntesis extra que causaba el error rojo en tu captura 09:03
    port_val = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port_val)