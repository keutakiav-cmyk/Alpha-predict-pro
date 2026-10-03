import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>⚡ ALPHA PREDICT PRO</title>
        <style>
            body { font-family: sans-serif; background-color: #0f1115; color: #ffffff; text-align: center; padding: 5px; }
            .navbar { background-color: #161b22; padding: 15px; font-size: 20px; font-weight: bold; color: #00ff88; border-bottom: 1px solid #30363d; }
            .container { max-width: 500px; margin: 20px auto; padding: 15px; }
            .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 15px; text-align: left; border-left: 5px solid #00ff88; }
            .btn { display: block; background-color: #00ff88; color: #000; padding: 12px; font-weight: bold; border-radius: 8px; text-decoration: none; margin: 15px 0; text-transform: uppercase; }
        </style>
    </head>
    <body>
        <div class="navbar">⚡ ALPHA PREDICT PRO v3.0</div>
        <div class="container">
            <a href="/" class="btn">🚀 ACTUALISER LES MATCHS</a>
            
            <h3 style="color: #8b949e; text-transform: uppercase; font-size: 14px;">📊 Opportunités du Jour</h3>
            
            <div class="card">
                <div style="font-size: 11px; color: #8b949e;">🏆 LIGUE DES NATIONS</div>
                <div style="font-weight: bold; font-size: 16px; margin: 5px 0;">⚽ Croatie - Angleterre</div>
                <div>🎯 Score Probable : <span style="color: #00ff88; font-weight: bold;">1 - 1</span></div>
                <div style="margin-top: 5px; font-size: 14px;">💡 Conseil : <b>GG (Oui)</b> (Fiabilité : 58.4%)</div>
            </div>

            <div class="card">
                <div style="font-size: 11px; color: #8b949e;">🏆 LIGUE DES NATIONS</div>
                <div style="font-weight: bold; font-size: 16px; margin: 5px 0;">⚽ Espagne - Tchéquie</div>
                <div>🎯 Score Probable : <span style="color: #00ff88; font-weight: bold;">2 - 0</span></div>
                <div style="margin-top: 5px; font-size: 14px;">💡 Conseil : <b>GN (Non)</b> (Fiabilité : 65.4%)</div>
            </div>

            <div class="card">
                <div style="font-size: 11px; color: #8b949e;">🏆 LIGUE DES NATIONS</div>
                <div style="font-weight: bold; font-size: 16px; margin: 5px 0;">⚽ Suisse - Slovénie</div>
                <div>🎯 Score Probable : <span style="color: #00ff88; font-weight: bold;">1 - 0</span></div>
                <div style="margin-top: 5px; font-size: 14px;">💡 Conseil : <b>GN (Non)</b> (Fiabilité : 61.2%)</div>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
