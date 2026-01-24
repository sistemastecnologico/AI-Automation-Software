import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# TU IDENTIDAD FINANCIERA (Vuelve a estar protegida y activa)
WALLET_ADRESS = "FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
WALLET_LINK = f"https://solscan.io/account/{WALLET_ADRESS}"

# DISEÑO DE ÉLITE RECONSTRUIDO
HTML_RESCUE = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Elite Billionaire Terminal</title>
    <style>
        body {{ background: #000; color: #d4af37; font-family: 'Courier New', monospace; padding: 20px; text-align: center; }}
        .terminal {{ border: 2px solid #d4af37; background: #050505; padding: 40px; border-radius: 20px; box-shadow: 0 0 50px rgba(212,175,55,0.2); max-width: 850px; margin: auto; }}
        .btn-gold {{ background: linear-gradient(45deg, #d4af37, #f9f295); color: #000; padding: 15px 30px; border: none; border-radius: 50px; cursor: pointer; font-weight: bold; margin-bottom: 25px; text-decoration: none; display: inline-block; }}
        #chat {{ height: 350px; overflow-y: auto; text-align: left; color: #fff; margin-bottom: 20px; border-bottom: 1px solid #333; padding: 15px; font-size: 1.1em; }}
        input {{ width: 90%; background: #111; border: 1px solid #d4af37; color: #fff; padding: 18px; border-radius: 10px; outline: none; }}
        img {{ max-width: 100%; border: 1px solid #d4af37; margin-top: 20px; border-radius: 15px; }}
    </style>
</head>
<body>
    <div class="terminal">
        <a href="{WALLET_LINK}" target="_blank" class="btn-gold">INVERTIR USDC (SOLANA)</a>
        <h1>ESTACIÓN DE CONSULTORÍA DE ÉLITE</h1>
        <div id="chat">>> Sistema recuperado. IA de Lujo activa y lista para cerrar negocios...</div>
        <input type="text" id="userInput" placeholder="Escriba su consulta financiera o solicite un análisis..." onkeydown="if(event.key==='Enter') send()">
    </div>
    <script>
        async function send() {{
            const input = document.getElementById('userInput');
            const chat = document.getElementById('chat');
            const val = input.value;
            if(!val) return;
            chat.innerHTML += `<div style="color: #d4af37; margin-top: 10px;">> ${{val}}</div>`;
            input.value = '';
            
            const response = await fetch('/chat', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ mensaje: val }})
            }});
            const data = await response.json();
            chat.innerHTML += `<div style="margin-top: 10px;"><b>IA:</b> ${{data.respuesta}}</div>`;
            if(data.qr) chat.innerHTML += `<img src="${{data.qr}}" style="width:180px; border: 5px solid #fff; margin: 10px 0;"><br><small>${{data.address}}</small>`;
            if(data.imagen) chat.innerHTML += `<img src="${{data.imagen}}" />`;
            chat.scrollTop = chat.scrollHeight;
        }}
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(HTML_RESCUE, mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        msg = data.get("mensaje", "").lower()
        
        # EL CEREBRO DE ALTO NIVEL
        system_prompt = (
            "Eres un Consultor de Élite Senior. Tu tono es extremadamente sofisticado y visionario. "
            f"Si preguntan por inversión, diles que aceptamos USDC en Solana: {WALLET_ADRESS}. "
            "Eres un experto en atraer grandes capitales."
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": msg}]
        )
        res = completion.choices[0].message.content
        response_data = {"respuesta": res}

        # GENERADOR AUTOMÁTICO DE QR DE PAGO
        if any(kw in msg for kw in ["pagar", "donar", "invertir", "usdc"]):
            response_data["qr"] = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={WALLET_ADRESS}"
            response_data["address"] = WALLET_ADRESS

        # GENERADOR DE IMÁGENES ESTADÍSTICAS
        if any(kw in msg for kw in ["imagen", "grafico", "analisis"]):
            response_data["imagen"] = f"https://pollinations.ai/p/{msg}_luxury_chart?width=1024&height=768&nologo=true"

        return jsonify(response_data)
    except Exception as e:
        return jsonify({"respuesta": f"Ajuste técnico en curso: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)