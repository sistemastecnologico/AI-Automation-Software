import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from groq import Groq
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# --- SEGURIDAD DE NIVEL EMPRESARIAL ---
# Esto asegura que Google reconozca tu web como segura (HTTPS)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "seguridad_maxima_2026")
CORS(app)

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
    # El parámetro _external=True es vital para trabajar remoto
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
        mensaje = request.json.get("mensaje")
        user = session.get('user', 'Invitado_Pro')
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Terminal Financiera Élite. Usuario: {user}. Portfolio: $10,000."},
                {"role": "user", "content": mensaje}
            ]
        )
        return jsonify({"respuesta": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"respuesta": f"Error de sistema: {str(e)}"})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)