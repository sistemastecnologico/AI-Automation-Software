import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from groq import Groq
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "vault_security_2026")
CORS(app)

# --- BASE DE DATOS (Ahorro de Datos) ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chats 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, mensaje TEXT, respuesta TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- SISTEMA DE IDENTIDAD ---
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def index():
    user = session.get('user')
    return render_template("dashboard.html", user=user)

@app.route('/login')
def login():
    return google.authorize_redirect(url_for('authorize', _external=True))

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session['user'] = user_info['email']
    return redirect(url_for('index'))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        mensaje = request.json.get("mensaje").lower()
        user_email = session.get('user', 'Invitado')
        
        # --- GENERADOR DE IMÁGENES/GRÁFICOS ---
        # Si el usuario pide un gráfico o reporte, generamos una "imagen" visual
        if "grafico" in mensaje or "reporte" in mensaje or "imagen" in mensaje:
            img_url = f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:['Ene','Feb','Mar'],datasets:[{{label:'Profit',data:[50,150,300]}}]}}}}"
            respuesta_ia = f"Generando reporte visual para {user_email}. Aquí tienes el análisis gráfico: <br><img src='{img_url}' style='width:100%; border-radius:8px; margin-top:10px;'>"
        else:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Eres una IA Financiera. Si el usuario logueado pide balances, usa el portfolio de $10,000."},
                    {"role": "user", "content": mensaje}
                ]
            )
            respuesta_ia = completion.choices[0].message.content

        # --- GUARDAR EN BASE DE DATOS ---
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chats (user, mensaje, respuesta) VALUES (?, ?, ?)", (user_email, mensaje, respuesta_ia))
        conn.commit()
        conn.close()

        return jsonify({"respuesta": respuesta_ia})
    except Exception as e:
        return jsonify({"respuesta": f"Error: {str(e)}"})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)