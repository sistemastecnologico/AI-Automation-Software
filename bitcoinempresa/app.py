from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_wtf.csrf import CSRFProtect, generate_csrf
import requests
import uuid

app = Flask(__name__)
app.secret_key = 'bitcoin2026'
csrf = CSRFProtect(app)

# Variables globales
balance_usd = 10000.00
wallets = {'BTC': 0.0, 'ETH': 0.0}
logs = []
cryptos = ['BTC', 'ETH']
sparklines = {}  # Diccionario vacío
total_donations_btc = 0.005  # Simulado
donation_address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"

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

@app.route("/", methods=['GET', 'POST'])
def login():
    return render_template('donations.html', total_donations=total_donations_btc, donation_address=donation_address)

@app.route("/dashboard")
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    crypto_data = {c: get_crypto_data(c) for c in cryptos}
    csrf_token = generate_csrf()
    acceso_premium = session.get('pago_realizado', False)
    return render_template('dashboard.html', balance=balance_usd, wallets=wallets, crypto_data=crypto_data, cryptos=cryptos, logs=logs, sparklines=sparklines, csrf_token=csrf_token, acceso_premium=acceso_premium)

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
    app.run(host='0.0.0.0', debug=True)

@app.route('/unlock_game', methods=['POST'])
def unlock_game():
    txid = request.form.get('txid')
    
    # Simulación de verificación de pago de $2 USD
    if txid and len(txid) >= 10:  # Verifica que el usuario puso un código
        session['pago_realizado'] = True
        # Aquí podrías agregar un log de auditoría
        logs.append(f'SISTEMA: Intento de acceso a Galaxia Premium detectado')
        return redirect(url_for('dashboard'))
    else:
        flash("Error: El TXID no ha sido confirmado en la red o es inválido.", "error")
        return redirect(url_for('dashboard'))
    