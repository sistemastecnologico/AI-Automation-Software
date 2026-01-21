from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
import requests
import threading
import time
import uuid

app = Flask(__name__)
app.secret_key = 'bitcoin2026'  # Clave secreta para sesiones
csrf = CSRFProtect(app)

# Variables globales
balance_usd = 10000.00
wallets = {'BTC': 0, 'ETH': 0}
logs = []
cryptos = ['BTC', 'ETH']

def get_crypto_data(symbol):
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/coins/{symbol.lower()}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false')
        data = response.json()
        market_data = data['market_data']
        return {
            'price': market_data['current_price']['usd'],
            'change_24h': market_data['price_change_percentage_24h'],
            'market_cap': market_data['market_cap']['usd']
        }
    except:
        return None

def get_crypto_sparkline(symbol):
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/coins/{symbol.lower()}/market_chart?vs_currency=usd&days=1&interval=hourly')
        data = response.json()
        prices = [p[1] for p in data['prices']]
        return prices[-24:]
    except:
        return []

def get_crypto_price(symbol):
    data = get_crypto_data(symbol)
    return data['price'] if data else None

def update_wallets():
    global balance_usd
    while True:
        for crypto in wallets:
            price = get_crypto_price(crypto)
            if price:
                # Actualizar balance basado en wallets, pero como es simulación, mantener balance_usd separado
                pass
        time.sleep(60)

# Inicializar
for crypto in cryptos:
    price = get_crypto_price(crypto)
    if price and crypto == 'BTC':
        wallets[crypto] = balance_usd / price
        break  # Solo inicializar BTC

price_thread = threading.Thread(target=update_wallets)
price_thread.daemon = True
price_thread.start()

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'bitcoin2026':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    crypto_data = {c: get_crypto_data(c) for c in cryptos}
    sparklines = {c: get_crypto_sparkline(c) for c in cryptos}
    csrf_token = generate_csrf()
    return render_template('dashboard.html', balance=balance_usd, wallets=wallets, crypto_data=crypto_data, sparklines=sparklines, cryptos=cryptos, logs=logs, csrf_token=csrf_token)

@app.route("/get_balance")
def get_balance():
    if not session.get('logged_in'):
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify({'balance': balance_usd})

@app.route('/buy', methods=['POST'])
def buy():
    crypto = request.form.get('crypto', '').upper()
    amount_str = request.form.get('amount', '')
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash('Cantidad inválida', 'error')
        return redirect(url_for('dashboard'))
    if crypto not in wallets:
        flash('Criptomoneda no soportada', 'error')
        return redirect(url_for('dashboard'))
    data = get_crypto_data(crypto)
    if not data:
        flash('Error obteniendo precio', 'error')
        return redirect(url_for('dashboard'))
    price = data['price']
    cost = amount * price
    if balance_usd >= cost:
        balance_usd -= cost
        wallets[crypto] += amount
        log_id = str(uuid.uuid4())
        logs.append({'id': log_id, 'message': f'Comprado {amount} {crypto} por ${cost:.2f}'})
        flash(f'Compra exitosa: {amount} {crypto}', 'success')
    else:
        flash('Fondos insuficientes', 'error')
    return redirect(url_for('dashboard'))

@app.route('/sell', methods=['POST'])
def sell():
    crypto = request.form.get('crypto', '').upper()
    amount_str = request.form.get('amount', '')
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash('Cantidad inválida', 'error')
        return redirect(url_for('dashboard'))
    if crypto not in wallets:
        flash('Criptomoneda no soportada', 'error')
        return redirect(url_for('dashboard'))
    if wallets[crypto] < amount:
        flash('No tienes suficientes criptomonedas', 'error')
        return redirect(url_for('dashboard'))
    data = get_crypto_data(crypto)
    if not data:
        flash('Error obteniendo precio', 'error')
        return redirect(url_for('dashboard'))
    price = data['price']
    revenue = amount * price
    balance_usd += revenue
    wallets[crypto] -= amount
    log_id = str(uuid.uuid4())
    logs.append({'id': log_id, 'message': f'Vendido {amount} {crypto} por ${revenue:.2f}'})
    flash(f'Venta exitosa: {amount} {crypto}', 'success')
    return redirect(url_for('dashboard'))

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)