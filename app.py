import os
import requests
from datetime import datetime
from flask import Flask, render_template_string

app = Flask(__name__)

API_KEY = "9f5c2c6459133767334f05de9c35a72d"

MATCHS_DATA = [
    {'ligue': 'Ligue des Nations', 'match': 'Croatie - Angleterre', 'c_safe': 1.42, 'p_safe': 'Double Chance 1X', 'c_mix': 3.10, 'p_mix': 'V2 & +2.5 buts (Victoire Angleterre)'},
    {'ligue': 'Ligue des Nations', 'match': 'Espagne - Tchéquie', 'c_safe': 1.48, 'p_safe': 'Plus de 1.5 buts', 'c_mix': 2.85, 'p_mix': 'V1 & Les deux marquent (Victoire Espagne)'},
    {'ligue': 'Ligue des Nations', 'match': 'Suisse - Slovénie', 'c_safe': 1.38, 'p_safe': 'Double Chance 1X', 'c_mix': 2.20, 'p_mix': 'Victoire Directe V1 (Suisse)'}
]

@app.route('/')
def dashboard():
    html_page = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>⚡ ALPHA PREDICT PRO</title>
        <style>
            body { font-family: sans-serif; background-color: #0f1115; color: #fff; padding: 15px; margin: 0; padding-bottom: 80px; }
            .navbar { background-color: #161b22; padding: 15px; font-weight: bold; color: #00ff88; text-align: center; border-bottom: 1px solid #30363d; font-size: 20px; }
            .section-title { font-size: 13px; color: #8b949e; text-transform: uppercase; margin: 20px 0 10px 0; font-weight: bold; border-left: 3px solid #00ff88; padding-left: 8px; }
            .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
            .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 60px; background-color: #161b22; border-top: 1px solid #30363d; display: grid; grid-template-columns: 1fr 1fr; }
            .nav-item { display: flex; flex-direction: column; align-items: center; justify-content: center; color: #8b949e; text-decoration: none; font-size: 11px; font-weight: bold; }
            .nav-item.active { color: #00ff88; background-color: rgba(0, 255, 136, 0.02); }
        </style>
    </head>
    <body>
        <div class="navbar">⚡ ALPHA PREDICT PRO</div>
        <div style="max-width: 500px; margin: 0 auto;">
            <div class="section-title">📊 Scanner Live Global</div>
            {% for m in liste_matchs %}
            <div class="card">
                <div style="font-size: 11px; color: #8b949e;">🏆 {{ m.ligue }}</div>
                <div style="font-weight: bold; font-size: 15px; margin: 5px 0;">⚽ {{ m.match }}</div>
                <div style="font-size: 13px; color: #00ff88;">🎯 Option Recommandée : <b>{{ m.p_safe }}</b> (Cote : {{ m.c_safe }})</div>
            </div>
            {% endfor %}
        </div>
        <div class="bottom-nav">
            <a href="/" class="nav-item active">🏠<br>Dashboard</a>
            <a href="/tickets" class="nav-item">🎯<br>Les 4 Combinés</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_page, liste_matchs=MATCHS_DATA)

@app.route('/tickets')
def tickets():
    cote_safe = round(MATCHS_DATA[0]['c_safe'] * MATCHS_DATA[1]['c_safe'] * MATCHS_DATA[2]['c_safe'], 2)
    cote_mix = round(MATCHS_DATA[0]['c_mix'] * MATCHS_DATA[1]['c_mix'], 2)
    
    html_page = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Les Tickets</title>
        <style>
            body {{ font-family: sans-serif; background-color: #0f1115; color: #fff; padding: 15px; margin: 0; padding-bottom: 80px; }}
            .navbar {{ background-color: #161b22; padding: 15px; font-weight: bold; color: #00ff88; text-align: center; border-bottom: 1px solid #30363d; font-size: 20px; }}
            .section-title {{ font-size: 13px; color: #8b949e; text-transform: uppercase; margin: 25px 0 10px 0; font-weight: bold; border-left: 3px solid #ffaa00; padding-left: 8px; }}
            .combine-box {{ background: linear-gradient(135deg, #1f2937 0%, #111827 100%); border: 2px solid #00ff88; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 15px; }}
            .combine-box.gold {{ border: 2px solid #ffaa00; }}
            .bottom-nav {{ position: fixed; bottom: 0; left: 0; right: 0; height: 60px; background-color: #161b22; border-top: 1px solid #30363d; display: grid; grid-template-columns: 1fr 1fr; }}
            .nav-item {{ display: flex; flex-direction: column; align-items: center; justify-content: center; color: #8b949e; text-decoration: none; font-size: 11px; font-weight: bold; }}
            .nav-item.active {{ color: #00ff88; background-color: rgba(0, 255, 136, 0.02); }}
        </style>
    </head>
    <body>
        <div class="navbar">⚡ ALPHA PREDICT PRO</div>
        <div style="max-width: 500px; margin: 0 auto;">
            
            <div class="section-title" style="border-left-color: #00ff88;">👑 1. Le Ticket Confiance (Safe)</div>
            <div class="combine-box">
                <div style="font-size: 28px; font-weight: bold; color: #00ff88;">Cote Globale : {cote_safe}</div>
                <p style="font-size: 13px; text-align: left; margin: 5px 0;">✔️ Croatie - Angleterre -> {MATCHS_DATA[0]['p_safe']} (Cote: {MATCHS_DATA[0]['c_safe']})</p>
                <p style="font-size: 13px; text-align: left; margin: 5px 0;">✔️ Espagne - Tchéquie -> {MATCHS_DATA[1]['p_safe']} (Cote: {MATCHS_DATA[1]['c_safe']})</p>
                <p style="font-size: 13px; text-align: left; margin: 5px 0;">✔️ Suisse - Slovénie -> {MATCHS_DATA[2]['p_safe']} (Cote: {MATCHS_DATA[2]['c_safe']})</p>
            </div>

            <div class="section-title">🔥 2. Le Combiné Grandes Cotes (Mix)</div>
            <div class="combine-box gold">
                <div style="font-size: 28px; font-weight: bold; color: #ffaa00;">Cote Globale : {cote_mix}</div>
                <p style="font-size: 13px; text-align: left; margin: 5px 0;">✔️ Croatie - Angleterre -> <b>{MATCHS_DATA[0]['p_mix']}</b></p>
                <p style="font-size: 13px; text-align: left; margin: 5px 0;">✔️ Espagne - Tchéquie -> <b>{MATCHS_DATA[1]['p_mix']}</b></p>
            </div>

            <div class="section-title" style="border-left-color: #00e1ff;">⚽ 3. Le Combiné Machine à Buts</div>
            <div class="combine-box" style="border-color: #00e1ff;">
                <div style="font-size: 24px; font-weight: bold; color: #00e1ff;">Cote Globale : 2.55</div>
                <p style="font-size: 13px; text-align: left; margin: 5px 0;">✔️ Plus de 1.5 buts sur les matchs sélectionnés</p>
            </div>

            <div class="section-title" style="border-left-color: #ff4b4b;">📐 4. Le Ticket Corners & Cartons</div>
            <div class="combine-box" style="border-color: #ff4b4b;">
                <div style="font-size: 24px; font-weight: bold; color: #ff4b4b;">Cote Globale : 3.40</div>
                <p style="font-size: 13px; text-align: left; margin: 5px 0;">✔️ Total Corners supérieur à 8.5 par rencontre</p>
            </div>

        </div>
        <div class="bottom-nav">
            <a href="/" class="nav-item">🏠<br>Dashboard</a>
            <a href="/tickets" class="nav-item active">🎯<br>Les 4 Combinés</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_page)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
