import os
from flask import Flask, render_template_string, redirect

app = Flask(__name__)

# Base de données de démonstration et d'historique
MATCHS_DATA = [
    {'ligue': 'Ligue des Nations', 'match': 'Croatie - Angleterre', 'score': '1-1', 'pari': 'GG (Oui)', 'fiabilite': 58.4, 'cote': 1.71},
    {'ligue': 'Ligue des Nations', 'match': 'Espagne - Tchéquie', 'score': '2-0', 'pari': 'GN (Non)', 'fiabilite': 65.4, 'cote': 1.53},
    {'ligue': 'Ligue des Nations', 'match': 'Suisse - Slovénie', 'score': '1-0', 'pari': 'GN (Non)', 'fiabilite': 61.2, 'cote': 1.63}
]

HISTORIQUE_DATA = [
    {'date': '02/10/2026', 'match': 'France - Italie', 'pari': 'GN (Non)', 'resultat': '1-0', 'statut': 'WIN', 'cote': 1.85},
    {'date': '01/10/2026', 'match': 'Lille - Real Madrid', 'pari': 'GN (Non)', 'resultat': '1-0', 'statut': 'WIN', 'cote': 2.10},
    {'date': '30/09/2026', 'match': 'Arsenal - PSG', 'pari': 'GG (Oui)', 'resultat': '2-1', 'statut': 'WIN', 'cote': 1.75},
    {'date': '26/09/2026', 'match': 'Atletico - Real Madrid', 'pari': 'GN (Non)', 'resultat': '1-1', 'statut': 'LOSE', 'cote': 1.95}
]

CSS_STYLE = """
<style>
    body { font-family: sans-serif; background-color: #0f1115; color: #f3f4f6; margin: 0; padding-bottom: 90px; }
    .navbar { background-color: #161b22; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; }
    .brand { font-size: 20px; font-weight: 800; color: #00ff88; }
    .main-container { max-width: 500px; margin: 20px auto; padding: 0 15px; }
    .section-title { font-size: 13px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; font-weight: 700; }
    .match-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 12px; overflow: hidden; }
    .card-header { background-color: #21262d; padding: 8px 16px; font-size: 11px; font-weight: 700; color: #8b949e; }
    .card-body { padding: 16px; }
    .teams-line { font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 12px; }
    .prediction-box { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background-color: #0f1115; padding: 12px; border-radius: 8px; border: 1px solid #30363d; }
    .pred-label { font-size: 11px; color: #8b949e; text-transform: uppercase; }
    .pred-value { font-size: 14px; font-weight: 700; color: #ffffff; margin-top: 2px; }
    .highlight { color: #00ff88; }
    .combine-box { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); border: 2px solid #00ff88; border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 20px; }
    .total-cote { font-size: 32px; font-weight: 900; color: #00ff88; margin: 10px 0; }
    .combine-item { background: rgba(255,255,255,0.03); padding: 10px; border-radius: 8px; margin: 8px 0; font-size: 14px; border-left: 3px solid #00ff88; }
    .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
    .stat-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; text-align: center; }
    .stat-number { font-size: 24px; font-weight: bold; color: #00ff88; }
    .history-row { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .badge-status { font-size: 11px; font-weight: 800; padding: 4px 8px; border-radius: 6px; }
    .status-win { background-color: rgba(0, 255, 136, 0.1); color: #00ff88; }
    .status-lose { background-color: rgba(255, 75, 75, 0.1); color: #ff4b4b; }
    .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 65px; background-color: #161b22; border-top: 1px solid #30363d; display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; z-index: 1000; }
    .nav-item { display: flex; flex-direction: column; align-items: center; justify-content: center; color: #8b949e; text-decoration: none; font-size: 10px; font-weight: 600; }
    .nav-item.active { color: #00ff88; background-color: rgba(0, 255, 136, 0.03); }
</style>
"""

NAV_BAR_HTML = '<div class="navbar"><div class="brand">⚡ ALPHA PREDICT PRO</div><div style="font-size:11px;color:#8b949e;">V3.0 FST STYLE</div></div>'

def generer_menu_bas(onglet_actif):
    return f'''
    <div class="bottom-nav">
        <a href="/" class="nav-item {'active' if onglet_actif == 'accueil' else ''}">🏠<br>Dashboard</a>
        <a href="/combine" class="nav-item {'active' if onglet_actif == 'combine' else ''}">🎯<br>Le Combiné</a>
        <a href="/bilan" class="nav-item {'active' if onglet_actif == 'bilan' else ''}">📈<br>Bilan (60j)</a>
        <a href="/methode" class="nav-item {'active' if onglet_actif == 'methode' else ''}">🧠<br>Méthode</a>
    </div>
    '''

@app.route('/')
def home():
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{CSS_STYLE}</head><body>{NAV_BAR_HTML}<div class="main-container"><div class="section-title">📊 Opportunités du jour</div>'''
    for m in MATCHS_DATA:
        html += f'''<div class="match-card"><div class="card-header">🏆 {m['ligue']}</div><div class="card-body"><div class="teams-line">⚽ {m['match']}</div><div class="prediction-box"><div><div class="pred-label">Score Probable</div><div class="pred-value highlight">{m['score']}</div></div><div><div class="pred-label">Pari conseillé</div><div class="pred-value">{m['pari']} ({m['fiabilite']}%)</div></div></div></div></div>'''
    html += f'''</div>{generer_menu_bas('accueil')}</body></html>'''
    return render_template_string(html)

@app.route('/combine')
def combine():
    cote_totale = 1.0
    for m in MATCHS_DATA:
        cote_totale *= m['cote']
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{CSS_STYLE}</head><body>{NAV_BAR_HTML}<div class="main-container"><div class="section-title">🎯 Le Combiné Safe du jour</div><div class="combine-box"><div style="font-size: 14px; text-transform: uppercase; color: #8b949e;">Cote Globale</div><div class="total-cote">{round(cote_totale, 2)}</div></div><div class="section-title">Détail des sélections :</div>'''
    for m in MATCHS_DATA:
        html += f'''<div class="combine-item"><b>⚽ {m['match']}</b><br><span style="font-size: 12px; color: #aaa;">Pari : {m['pari']} | Cote : {m['cote']}</span></div>'''
    html += f'''</div>{generer_menu_bas('combine')}</body></html>'''
    return render_template_string(html)

@app.route('/bilan')
def bilan():
    total_matchs = len(HISTORIQUE_DATA)
    victoires = sum(1 for m in HISTORIQUE_DATA if m['statut'] == 'WIN')
    taux = (victoires / total_matchs) * 100
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{CSS_STYLE}</head><body>{NAV_BAR_HTML}<div class="main-container"><div class="section-title">📈 Historique de rentabilité</div><div class="stats-grid"><div class="stat-card"><div class="pred-label">Matchs Gagnés</div><div class="stat-number">{victoires}/{total_matchs}</div></div><div class="stat-card"><div class="pred-label">Taux Réussite</div><div class="stat-number">{round(taux, 1)}%</div></div></div>'''
    for m in HISTORIQUE_DATA:
        html += f'''<div class="history-row"><div><span style="font-size:11px;color:#8b949e;">🗓️ {m['date']}</span><div style="font-weight:bold;font-size:14px;margin-top:2px;">{m['match']}</div><span style="font-size:12px;color:#aaa;">Pari : <b>{m['pari']}</b> | Score : {m['resultat']}</span></div><div><span class="badge-status {'status-win' if m['statut'] == 'WIN' else 'status-lose'}">{'✅ GAGNÉ' if m['statut'] == 'WIN' else '❌ PERDU'}</span></div></div>'''
    html += f'''</div>{generer_menu_bas('bilan')}</body></html>'''
    return render_template_string(html)

@app.route('/methode')
def methode():
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{CSS_STYLE}</head><body>{NAV_BAR_HTML}<div class="main-container"><div class="section-title">🧠 Algorithme Mathématique</div><div style="background-color:#161b22;border:1px solid #30363d;padding:20px;border-radius:12px;line-height:1.6;font-size:14px;color:#e1e1e1;">Calcul automatique des probabilités via la <b>Loi de Poisson</b> pour isoler les Value Bets quotidiens et garantir la stabilité à long terme.</div></div>{generer_menu_bas('methode')}</body></html>'''
    return render_template_string(html)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
