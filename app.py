import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# CONFIGURACIÓN DE ÉLITE
W_ADDR = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
G_ID = "1003655956505-nh7tso7hb4acuk77489pf9p08far0d9u.apps.googleusercontent.com"

# Interfaz simplificada para evitar errores de sintaxis
UI = f"""
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>CORE SYSTEM | ELITE</title>
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
    :root {{ --n: #00f2ff; --bg: #050505; }}
    body {{ background: var(--bg); color: #fff; font-family: sans-serif; margin: 0; text-align: center; }}
    .h {{ height: 40vh; display: flex; flex-direction: column; justify-content: center; background: radial-gradient(circle, #0a192f, #000); border-bottom: 1px solid #333; }}
    .t {{ width: 90%; max-width: 900px; margin: 20px auto; padding: 20px; background: #111; border-radius: 10px; border: 1px solid #444; }}
    #c {{ height: 250px; overflow-y: auto; color: var(--n); font-family: monospace; text-align: left; padding: 10px; }}
    input {{ width: 100%; background: #000; border: 1px solid #333; color: #fff; padding: 15px; margin-top: 10px; outline: none; }}
    .btn {{ padding: 10px 25px; background: var(--n); color: #000; border-radius: 5px; text-decoration: none; font-weight: bold; display: inline-block; margin: 10px; }}
</style></head>
<body>
    <div style="position:fixed; top:10px; right:10px;">
        <div id="g_id_onload" data-client_id="{G_ID}" data-callback="hA"></div>
        <div class="g_id_signin" data-type="icon"></div>
    </div>
    <header class="h">
        <h1 style="letter-spacing:10px;">QUANTUM CORE</h1>
        <p style="color:gray;">IA INDUSTRIAL • BLOCKCHAIN • SCIENCE</p>
        <div><a href="https://solscan.io/account/{W_ADDR}" target="_blank" class="btn">BLOCKCHAIN</a></div>
    </header>
    <div class="t">
        <div id="c">>> SISTEMA LISTO.</div>
        <input type="text" id="i" placeholder="Escriba requerimiento..." onkeydown="if(event.key==='Enter') exe()">
        <div id="p" style="height:250px; margin-top:20px;"></div>
    </div>
    <script>
        function hA(r) {{ console.log("OK"); }}
        Plotly.newPlot('p', [{{ x:[1,2,3,4], y:[10,15,13,17], type:'scatter', line:{{color:'#00f2ff'}} }}], {{ paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{{color:'#fff'}}, margin:{{t:0,b:30,l:30,r:10}} }});
        async function exe() {{
            const i=document.getElementById('i'), c=document.getElementById('c'); if(!i.value) return;
            const m=i.value; i.value=''; c.innerHTML += `<div>> USER: ${{m}}</div>`;
            const r=await fetch('/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{mensaje:m}})}});
            const d=await r.json(); c.innerHTML += `<div style="color:#fff;">> AI: ${{d.respuesta}}</div>`;
            if(d.qr) c.innerHTML += `<img src="${{d.qr}}" style="width:150px; margin-top:10px; border:1px solid var(--n);">`;
            c.scrollTop=c.scrollHeight;
        }}
    </script>
</body></html>
"""

@app.route("/")
def index():
    return Response(UI, mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        msg = data.get("mensaje", "").lower()
        sys = f"IA de élite. Wallet: {W_ADDR}."
        comp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":sys},{"role":"user","content":msg}])
        res = comp.choices[0].message.content
        out = {"respuesta": res}
        if any(x in msg for x in ["pago", "contratar", "solana"]):
            out["qr"] = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={W_ADDR}"
        return jsonify(out)
    except Exception as e:
        return jsonify({"respuesta": f"ERR: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))