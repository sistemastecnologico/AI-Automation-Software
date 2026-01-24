import os
from flask import Flask, request, jsonify, Response
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# TU LINK DE USDC SOLANA INTEGRADO
WALLET_LINK = "https://solscan.io/account/FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"

HTML_FINAL = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Billionaire Workstation</title>
    <style>
        body {{ background: #000; color: #d4af37; font-family: monospace; padding: 20px; text-align: center; }}
        .terminal {{ border: 2px solid #d4af37; background: #050505; padding: 30px; border-radius: 15px; box-shadow: 0 0 40px #1a1a1a; max-width: 850px; margin: auto; }}
        .btn-gold {{ background: linear-gradient(45deg, #d4af37, #f9f295); color: #000; padding: 15px 30px; border: none; font-weight: bold; cursor: pointer; border-radius: 50px; margin-bottom: 25px; font-size: 1.1em; }}
        #chat {{ height: 350px; overflow-y: auto; text-align: left; color: #fff; margin-bottom: 20px; border-bottom: 1px solid #333; padding: 15px; font-size: 0.9em; }}
        input {{ width: 90%; background: #111; border: 1px solid #d4af37; color: #fff; padding: 18px; border-radius: 10px; outline: none; }}
        img {{ max-width: 100%; border: 1px solid #d4af37; margin-top: 15px; border-radius: 10px; }}
    </style>
</head>
<body>
    <div class="terminal">
        <button class="btn-gold" onclick="window.open('{WALLET_LINK}', '_blank')">APOYAR PROYECTO (USDC SOLANA)</button>
        <h1>SISTEMA DE ÉLITE V1.0</h1>
        <p style="color: #666;">Consultoría Técnica | Finanzas | Ciencia | IA</p>
        <div id="chat">>> Terminal Segura Iniciada. Su wallet USDC está vinculada correctamente.</div>
        <input type="text" id="userInput" placeholder="Pida consultoría o gráficos financieros..." onkeydown="if(event.key==='Enter') sendMessage()">
    </div>
    <script>
        async function sendMessage() {{
            const input = document.getElementById('userInput');
            const chat = document.getElementById('chat');
            const userMsg = input.value;
            chat.innerHTML += `<div style="color: #d4af37;">> ${{userMsg}}</div>`;
            input.value = '';
            
            const response = await fetch('/chat', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ mensaje: userMsg }})
            }});
            const data = await response.json();
            chat.innerHTML += `<div>${{data.respuesta}}</div>`;
            if(data.imagen) chat.innerHTML += `<img src="${{data.imagen}}" />`;
            chat.scrollTop = chat.scrollHeight;
        }}
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(HTML_FINAL, mimetype='text/html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        msg = data.get("mensaje", "").lower()
        
        # IA CONFIGURADA PARA RECORDAR TU WALLET Y VENDER TUS SERVICIOS
        prompt = f"Eres una IA de élite. Si preguntan por pagos o donar, indica que aceptamos USDC en Solana: FN5nJbDwC5ySkaUaaYqKFqvL2FsVju9xMsv6tzZGLxp"
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{{"role": "system", "content": prompt}}, {{"role": "user", "content": msg}}]
        )
        res = completion.choices[0].message.content

        # GENERADOR DE IMÁGENES ÚTILES (ESTADÍSTICAS)
        if any(kw in msg for kw in ["imagen", "grafico", "estadistica"]):
            url = f"https://pollinations.ai/p/{msg}_financial_luxury_chart?width=1024&height=768&nologo=true"
            return jsonify({{"respuesta": res, "imagen": url}})

        return jsonify({{"respuesta": res}})
    except Exception as e:
        return jsonify({{"respuesta": f"Error: {{str(e)}}"}}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)