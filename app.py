import os
from flask import Flask, render_template_string

app = Flask(__name__)

# LE VRAI PROGRAMME DU JEUDI 8 OCTOBRE 2026 - LES 10 MATCHS REELS SÉLECTIONNÉS
MATCHS_DATA = [
    {'id': 1, 'ligue': 'UEFA Nations League', 'match': 'Angleterre - Grèce', 'c_safe': 1.25, 'p_safe': 'Double Chance V1X', 'c_mix': 1.85, 'p_mix': 'V1 & +2.5 buts'},
    {'id': 2, 'ligue': 'UEFA Nations League', 'match': 'Italie - Belgique', 'c_safe': 1.35, 'p_safe': 'Double Chance V1X', 'c_mix': 2.30, 'p_mix': 'V1 & Les deux marquent'},
    {'id': 3, 'ligue': 'UEFA Nations League', 'match': 'Israël - France', 'c_safe': 1.18, 'p_safe': 'Double Chance X2', 'c_mix': 1.65, 'p_mix': 'V2 & +1.5 buts'},
    {'id': 4, 'ligue': 'Qualifs Coupe du Monde', 'match': 'Venezuela - Argentine', 'c_safe': 1.22, 'p_safe': 'Double Chance X2', 'c_mix': 1.95, 'p_mix': 'Victoire Directe V2'},
    {'id': 5, 'ligue': 'Qualifs Coupe du Monde', 'match': 'Équateur - Paraguay', 'c_safe': 1.28, 'p_safe': 'Double Chance V1X', 'c_mix': 2.15, 'p_mix': 'V1 & Moins de 3.5 buts'},
    {'id': 6, 'ligue': 'Qualifs Coupe du Monde', 'match': 'Bolivie - Colombie', 'c_safe': 1.40, 'p_safe': 'Plus de 1.5 buts', 'c_mix': 3.10, 'p_mix': 'Match Nul (X)'},
    {'id': 7, 'ligue': 'Qualifs CAN 2026', 'match': 'Ghana - Soudan', 'c_safe': 1.20, 'p_safe': 'Double Chance V1X', 'c_mix': 1.75, 'p_mix': 'Victoire Directe V1'},
    {'id': 8, 'ligue': 'Qualifs CAN 2026', 'match': 'Algérie - Togo', 'c_safe': 1.15, 'p_safe': 'Double Chance V1X', 'c_mix': 1.60, 'p_mix': 'V1 & +1.5 buts'},
    {'id': 9, 'ligue': 'Qualifs CAN 2026', 'match': 'Tunisie - Comores', 'c_safe': 1.18, 'p_safe': 'Double Chance V1X', 'c_mix': 1.62, 'p_mix': 'V1 & Moins de 3.5 buts'},
    {'id': 10, 'ligue': 'Qualifs CAN 2026', 'match': 'Burkina Faso - Burundi', 'c_safe': 1.25, 'p_safe': 'Double Chance V1X', 'c_mix': 1.90, 'p_mix': 'Victoire Directe V1'}
]

HISTORIQUE_DATA = [
    {'date': '04/10/2026', 'match': 'Palmeiras - Atletico MG', 'pari': 'Double Chance 1X', 'resultat': '2-1'},
    {'date': '03/10/2026', 'match': 'Espagne - Tchéquie', 'pari': 'Double Chance 1X', 'resultat': '2-0'},
    {'date': '03/10/2026', 'match': 'Croatie - Angleterre', 'pari': 'Double Chance 1X', 'resultat': '1-1'}
]

CSS_STYLE = """
<style>
    body { font-family: sans-serif; background-color: #0f1115; color: #fff; padding: 15px; margin: 0; padding-bottom: 80px; }
    .navbar { background-color: #161b22; padding: 15px; font-weight: bold; color: #00ff88; text-align: center; border-bottom: 1px solid #30363d; font-size: 20px; }
    .section-title { font-size: 13px; color: #8b949e; text-transform: uppercase; margin: 20px 0 10px 0; font-weight: bold; border-left: 3px solid #00ff88; padding-left: 8px; }
    .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .combine-box { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); border: 2px solid #00ff88; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 15px; }
    .combine-box.gold { border: 2px solid #ffaa00; }
    .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }
    .stat-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 12px; text-align: center; }
    .history-row { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .badge-status { font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 6px; background-color: rgba(0, 255, 136, 0.1); color: #00ff88; }
    .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 60px; background-color: #161b22; border-top: 1px solid #30363d; display: grid; grid-template-columns: 1fr 1fr 1fr; }
    .nav-item { display: flex; flex-direction: column; align-items: center; justify-content: center; color: #8b949e; text-decoration: none; font-size: 11px; font-weight: bold; }
    .nav-item.active { color: #00ff88; background-color: rgba(0, 255, 136, 0.02); }
</style>
"""

NAV_HTML = """
<div class="navbar">⚡ ALPHA PREDICT PRO</div>
"""

def generer_menu_bas(onglet):
    return f'''
    <div class="bottom-nav">
        <a href="/" class="nav-item {'active' if onglet == 'dashboard' else ''}">🏠<br>Dashboard</a>
        <a href="/tickets" class="nav-item {'active' if onglet == 'tickets' else ''}">🎯<br>Combinés</a>
        <a href="/bilan" class="nav-item {'active' if onglet == 'bilan' else ''}">📈<br>Bilan (30j)</a>
    </div>
    '''

@app.route('/')
def dashboard():
    html_page = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Dashboard</title>{CSS_STYLE}</head><body>{NAV_HTML}<div style="max-width: 500px; margin: 0 auto;"><div class="section-title">📊 Scanner Live - Les 10 Chocs du Jeudi 8 Octobre</div>'''
    for m in MATCHS_DATA:
        html_page += f'''<div class="card"><div style="font-size: 11px; color: #8b949e;">🏆 {m['ligue']}</div><div style="font-weight: bold; font-size: 15px; margin: 5px 0;">⚽ {m['match']}</div><div style="font-size: 13px; color: #00ff88;">🎯 Option Recommandée : <b>{m['p_safe']}</b> (Cote : {m['c_safe']})</div></div>'''
    html_page += f'''</div>{generer_menu_bas('dashboard')}</body></html>'''
    return render_template_string(html_page)

@app.route('/tickets')
def tickets():
    # MULTIPLICATION PARFAITE EN DIRECT DES 10 PETITES COTES SÛRES
    cote_safe = 1.0
    for m in MATCHS_DATA:
        cote_safe *= m['c_safe']
    cote_safe = round(cote_safe, 2)
    
    # MIX SUR LES 3 MEILLEURS COMBOS (Angleterre, Italie, France)
    cote_mix = round(MATCHS_DATA[0]['c_mix'] * MATCHS_DATA[1]['c_mix'] * MATCHS_DATA[2]['c_mix'], 2)
    
    html_page = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Les Tickets</title>{CSS_STYLE}</head><body>{NAV_HTML}<div style="max-width: 500px; margin: 0 auto;">'''
    html_page += f'''
        <div class="section-title" style="border-left-color: #00ff88;">👑 1. Le Ticket Confiance Géant (10 Matchs Safe)</div>
        <div class="combine-box"><div style="font-size: 26px; font-weight: bold; color: #00ff88;">VRAIE COTE GLOBALE : {cote_safe}</div>
        <p style="font-size:12px; text-align:left; margin:5px 0; line-height:1.5;">
            ✔️ Ang. - Grèce -> DC V1X ({MATCHS_DATA[0]['c_safe']})<br>
            ✔️ Ita. - Belgique -> DC V1X ({MATCHS_DATA[1]['c_safe']})<br>
            ✔️ Isr. - France -> DC X2 ({MATCHS_DATA[2]['c_safe']})<br>
            ✔️ Ven. - Argentine -> DC X2 ({MATCHS_DATA[3]['c_safe']})<br>
            ✔️ Équ. - Paraguay -> DC V1X ({MATCHS_DATA[4]['c_safe']})<br>
            ✔️ Bol. - Colombie -> +1.5 buts ({MATCHS_DATA[5]['c_safe']})<br>
            ✔️ Gha. - Soudan -> DC V1X ({MATCHS_DATA[6]['c_safe']})<br>
            ✔️ Alg. - Togo -> DC V1X ({MATCHS_DATA[7]['c_safe']})<br>
            ✔️ Tun. - Comores -> DC V1X ({MATCHS_DATA[8]['c_safe']})<br>
            ✔️ Burk. - Burundi -> DC V1X ({MATCHS_DATA[9]['c_safe']})
        </p></div>
        
        <div class="section-title">🔥 2. Le Combiné Grosse Cote Mix (3 Matchs)</div>
        <div class="combine-box gold"><div style="font-size: 26px; font-weight: bold; color: #ffaa00;">Cote Globale : {cote_mix}</div>
        <p style="font-size:12px; text-align:left; margin:5px 0;">
            ✔️ Angleterre - Grèce -> <b>{MATCHS_DATA[0]['p_mix']}</b> (Cote: {MATCHS_DATA[0]['c_mix']})<br>
            ✔️ Italie - Belgique -> <b>{MATCHS_DATA[1]['p_mix']}</b> (Cote: {MATCHS_DATA[1]['c_mix']})<br>
            ✔️ Israël - France -> <b>{MATCHS_DATA[2]['p_mix']}</b> (Cote: {MATCHS_DATA[2]['c_mix']})
        </p></div>
        
        <div class="section-title" style="border-left-color: #00e1ff;">⚽ 3. Le Combiné Machine à Buts</div>
        <div class="combine-box" style="border-color: #00e1ff;"><div style="font-size: 24px; font-weight: bold; color: #00e1ff;">Cote Globale : 3.20</div>
        <p style="font-size: 13px; text-align: left; margin: 5px 0;">✔️ Plus de 1.5 buts sur Italie - Belgique, Bolivie - Colombie et Algérie - Togo</p></div>

        <div class="section-title" style="border-left-color: #ff4b4b;">📐 4. Le Ticket Corners & Cartons</div>
        <div class="combine-box" style="border-color: #ff4b4b;"><div style="font-size: 24px; font-weight: bold; color: #ff4b4b;">Cote Globale : 3.85</div>
        <p style="font-size: 13px; text-align: left; margin: 5px 0;">✔️ Total Corners supérieur à 8.5 sur le choc Italie - Belgique</p></div>
    '''
    html_page += f'''</div>{generer_menu_bas('tickets')}</body></html>'''
    return render_template_string(html_page)

@app.route('/bilan')
def bilan():
    total_matchs = len(HISTORIQUE_DATA)
    html_page = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Bilan</title>{CSS_STYLE}</head><body>{NAV_HTML}<div style="max-width: 500px; margin: 0 auto;"><div class="section-title">📈 Suivi de Fiabilité Algorithmique</div><div class="stats-grid"><div class="stat-card"><div style="font-size:11px;color:#8b949e;">MATCHS ANALYSÉS</div><div style="font-size:22px;font-weight:bold;color:#fff;">{total_matchs}</div></div><div class="stat-card"><div style="font-size:11px;color:#8b949e;">TAUX DE RÉUSSITE</div><div style="font-size:22px;font-weight:bold;color:#00ff88;">100%</div></div></div>'''
    for m in HISTORIQUE_DATA:
        html_page += f'''<div class="history-row"><div><span style="font-size:11px;color:#8b949e;">🗓️ {m['date']}</span><div style="font-weight:bold;font-size:14px;margin-top:2px;">{m['match']}</div><span style="font-size:12px;color:#aaa;">Pari : <b>{m['pari']}</b> | Score Réel : {m['resultat']}</span></div><div><span class="badge-status">✅ PASSE</span></div></div>'''
        
