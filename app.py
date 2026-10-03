import os
from flask import Flask, render_template_string, redirect

app = Flask(__name__)

# Base de données d'analyses enrichie avec marchés avancés pour alimenter les 4 combinés
MATCHS_DATA = [
    {'ligue': 'Ligue des Nations', 'match': 'Espagne - Tchéquie', 'pari_safe': 'Double Chance 1X', 'prob_safe': 88.5, 'cote_safe': 1.15, 'pari_buts': 'Les deux marquent : NON', 'cote_buts': 1.65, 'pari_combo': 'Victoire Espagne & Non GG', 'cote_combo': 2.10, 'pari_speciaux': 'Plus de 8.5 Corners', 'cote_speciaux': 1.45},
    {'ligue': 'Ligue des Nations', 'match': 'Suisse - Slovénie', 'pari_safe': 'Moins de 3.5 buts', 'prob_safe': 82.1, 'cote_safe': 1.25, 'pari_buts': 'Moins de 2.5 buts', 'cote_buts': 1.60, 'pari_combo': 'Suisse gagne par 1 but exact', 'cote_combo': 3.15, 'pari_speciaux': 'Moins de 4.5 Cartons', 'cote_speciaux': 1.60},
    {'ligue': 'Ligue des Nations', 'match': 'Cameroun - Égypte', 'pari_safe': 'Double Chance 1X', 'prob_safe': 81.2, 'cote_safe': 1.22, 'pari_buts': 'Moins de 2.5 buts', 'cote_buts': 1.55, 'pari_combo': 'Match Nul à la mi-temps', 'cote_combo': 1.95, 'pari_speciaux': 'Plus de 3.5 Cartons', 'cote_speciaux': 1.50},
    {'ligue': 'Ligue des Nations', 'match': 'Croatie - Angleterre', 'pari_safe': 'Plus de 1.5 buts', 'prob_safe': 76.4, 'cote_safe': 1.32, 'pari_buts': 'Les deux marquent : OUI', 'cote_buts': 1.80, 'pari_combo': 'Victoire Angleterre', 'cote_combo': 2.25, 'pari_speciaux': 'Plus de 9.5 Corners', 'cote_speciaux': 1.70}
]

HISTORIQUE_DATA = [
    {'date': '02/10/2026', 'match': 'France - Italie', 'pari': 'Double Chance 1X', 'resultat': '1-0', 'statut': 'WIN'},
    {'date': '01/10/2026', 'match': 'Lille - Real Madrid', 'pari': 'Moins de 3.5 buts', 'resultat': '1-0', 'statut': 'WIN'},
    {'date': '30/09/2026', 'match': 'Arsenal - PSG', 'pari': 'Plus de 1.5 buts', 'resultat': '2-1', 'statut': 'WIN'}
]

CSS_STYLE = """
<style>
    body { font-family: sans-serif; background-color: #0f1115; color: #f3f4f6; margin: 0; padding-bottom: 90px; }
    .navbar { background-color: #161b22; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; }
    .brand { font-size: 20px; font-weight: 800; color: #00ff88; }
    .main-container { max-width: 500px; margin: 20px auto; padding: 0 15px; }
    .section-title { font-size: 13px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-top: 25px; margin-bottom: 15px; font-weight: 700; border-left: 3px solid #00ff88; padding-left: 8px; }
    .match-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 12px; overflow: hidden; }
    .card-header { background-color: #21262d; padding: 8px 16px; font-size: 11px; font-weight: 700; color: #8b949e; }
    .card-body { padding: 16px; }
    .teams-line { font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 12px; }
    .prediction-box { display: grid; grid-template-columns: 1fr; gap: 8px; background-color: #0f1115; padding: 12px; border-radius: 8px; border: 1px solid #30363d; }
    .pred-item { display: flex; justify-content: space-between; align-items: center; font-size: 13px; border-bottom: 1px solid #222; padding-bottom: 4px; }
    .pred-label { color: #8b949e; text-transform: uppercase; font-size: 11px; }
    .highlight { color: #00ff88; font-weight: bold; }
    
    .combine-box { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); border: 1px solid #30363d; border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 15px; position: relative; overflow: hidden; }
    .combine-box.premium { border: 2px solid #00ff88; }
    .combine-box.gold { border: 2px solid #ffaa00; }
    .total-cote { font-size: 32px; font-weight: 900; color: #00ff88; margin: 8px 0; }
    .total-cote.gold { color: #ffaa00; }
    .combine-item { background: rgba(255,255,255,0.02); padding: 10px; border-radius: 8px; margin: 8px 0; font-size: 13px; text-align: left; border-left: 3px solid #444; }
    .combine-item.premium { border-left: 3px solid #00ff88; }
    .combine-item.gold { border-left: 3px solid #ffaa00; }
    
    .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
    .stat-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; text-align: center; }
    .stat-number { font-size: 24px; font-weight: bold; color: #00ff88; }
    .history-row { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .badge-status { font-size: 11px; font-weight: 800; padding: 4px 8px; border-radius: 6px; background-color: rgba(0, 255, 136, 0.1); color: #00ff88; }
    .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 65px; background-color: #161b22; border-top: 1px solid #30363d; display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; z-index: 1000; }
    .nav-item { display: flex; flex-direction: column; align-items: center; justify-content: center; color: #8b949e; text-decoration: none; font-size: 10px; font-weight: 600; text-align: center; }
    .nav-item.active { color: #00ff88; background-color: rgba(0, 255, 136, 0.03); }
</style>
"""

NAV_BAR_HTML = '<div class="navbar"><div class="brand">⚡ ALPHA PREDICT PRO</div><div style="font-size:11px;color:#8b949e;">V5.0 MULTI-TICKETS</div></div>'

def generer_menu_bas(onglet_actif):
    return f'''
    <div class="bottom-nav">
        <a href="/" class="nav-item {'active' if onglet_actif == 'accueil' else ''}">🏠<br>Dashboard</a>
        <a href="/combine" class="nav-item {'active' if onglet_actif == 'combine' else ''}">🎯<br>Les Combinés</a>
        <a href="/bilan" class="nav-item {'active' if onglet_actif == 'bilan' else ''}">📈<br>Bilan (60j)</a>
        <a href="/methode" class="nav-item {'active' if onglet_actif == 'methode' else ''}">🧠<br>Méthode</a>
    </div>
    '''

@app.route('/')
def home():
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{CSS_STYLE}</head><body>{NAV_BAR_HTML}<div class="main-container"><div class="section-title">📊 Analyses Multi-Marchés par Match</div>'''
    for m in MATCHS_DATA:
        html += f'''
        <div class="match-card">
            <div class="card-header">🏆 {m['ligue']}</div>
            <div class="card-body">
                <div class="teams-line">⚽ {m['match']}</div>
                <div class="prediction-box">
                    <div class="pred-item"><span class="pred-label">Sécurité (1X2/Buts)</span><span class="highlight">{m['pari_safe']}</span></div>
                    <div class="pred-item"><span class="pred-label">Marché Buts / GG</span><span>{m['pari_buts']}</span></div>
                    <div class="pred-item"><span class="pred-label">Corners / Cartons</span><span>{m['pari_speciaux']}</span></div>
                </div>
            </div>
        </div>
        '''
    html += f'''</div>{generer_menu_bas('accueil')}</body></html>'''
    return render_template_string(html)

@app.route('/combine')
def combine():
    # 1. Calcul Ticket Confiance (Espagne + Suisse + Cameroun en Safe)
    c_confiance = round(MATCHS_DATA[0]['cote_safe'] * MATCHS_DATA[1]['cote_safe'] * MATCHS_DATA[2]['cote_safe'], 2)
    
    # 2. Calcul Ticket Machine à Buts (Croatie + Espagne en Buts)
    c_buts = round(MATCHS_DATA[3]['cote_buts'] * MATCHS_DATA[0]['cote_buts'], 2)
    
    # 3. Calcul Ticket Corners & Cartons
    c_speciaux = round(MATCHS_DATA[0]['pari_speciaux' != ''] * MATCHS_DATA[1]['cote_speciaux'] * MATCHS_DATA[2]['cote_speciaux'] * MATCHS_DATA[3]['cote_speciaux'] * 0.7, 2)
    
    # 4. Calcul Ticket Grosse Cote Spéculatif (Espagne Combo + Suisse Combo + Croatie Victoire)
    c_grosse = round(MATCHS_DATA[0]['cote_combo'] * MATCHS_DATA[1]['cote_combo'] * MATCHS_DATA[3]['cote_combo'], 2)
        
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{CSS_STYLE}</head><body>{NAV_BAR_HTML}<div class="main-container">
        
        <div class="section-title">👑 1. Le Ticket Confiance du Jour</div>
        <div class="combine-box premium">
            <div style="font-size: 12px; text-transform: uppercase; color: #8b949e;">Indice de Stabilité Élevé</div>
            <div class="total-cote">Cote : {c_confiance}</div>
        </div>
        <div class="combine-item premium"><b>⚽ Espagne - Tchéquie</b><br><span style="font-size:11px;color:#aaa;">Pari : {MATCHS_DATA[0]['pari_safe']} | Cote : {MATCHS_DATA[0]['cote_safe']}</span></div>
        <div class="combine-item premium"><b>⚽ Suisse - Slovénie</b><br><span style="font-size:11px;color:#aaa;">Pari : {MATCHS_DATA[1]['pari_safe']} | Cote : {MATCHS_DATA[1]['cote_safe']}</span></div>
        <div class="combine-item premium"><b>⚽ Cameroun - Égypte</b><br><span style="font-size:11px;color:#aaa;">Pari : {MATCHS_DATA[2]['pari_safe']} | Cote : {MATCHS_DATA[2]['cote_safe']}</span></div>
        
        <div class="section-title">⚽ 2. Le Combiné Machine à Buts</div>
        <div class="combine-box">
            <div class="total-cote" style="color:#ffffff;">Cote : {c_buts}</div>
        </div>
        <div class="combine-item"><b>⚽ Croatie - Angleterre</b><br><span style="font-size:11px;color:#aaa;">Pari : {MATCHS_DATA[3]['pari_buts']} | Cote : {MATCHS_DATA[3]['cote_buts']}</span></div>
        <div class="combine-item"><b>⚽ Espagne - Tchéquie</b><br><span style="font-size:11px;color:#aaa;">Pari : {MATCHS_DATA[0]['pari_buts']} | Cote : {MATCHS_DATA[0]['cote_buts']}</span></div>
        
        <div class="section-title">📐 3. Le Ticket Corners & Cartons</div>
        <div class="combine-box">
            <div class="total-cote" style="color:#00e1ff;">Cote : {c_speciaux}</div>
        </div>
    
