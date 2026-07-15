import numpy as np
from flask import Flask, request, render_template_string
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, roc_auc_score
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# ==========================================
# INITIAL INDIAN FINTECH DATASET
# ==========================================
np.random.seed(42)

# 300 Normal Transactions (UPI / Domestic Cards)
legit_features = np.random.multivariate_normal(
    mean=[1200, 14, 1.1], 
    cov=[[300000, 0, 0], [0, 8, 0], [0, 0, 0.2]], 
    size=300
)
# 15 Advanced Fraud Transactions (Mule Account Transfers / Scams)
fraud_features = np.random.multivariate_normal(
    mean=[85000, 3, 7.9], 
    cov=[[60000000, 0, 0], [0, 3, 0], [0, 0, 0.6]], 
    size=15
)

X_raw = np.vstack([legit_features, fraud_features])
y_raw = np.array([0] * 300 + [1] * 15)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)

model = LogisticRegression(class_weight=None)
model.fit(X_scaled, y_raw)

smote_enabled = False
metrics = {"precision": 0.0, "recall": 0.0, "roc_auc": 0.0}

def update_metrics():
    preds = model.predict(X_scaled)
    probs = model.predict_proba(X_scaled)[:, 1]
    metrics["precision"] = round(precision_score(y_raw, preds, zero_division=0) * 100, 1)
    metrics["recall"] = round(recall_score(y_raw, preds, zero_division=0) * 100, 1)
    metrics["roc_auc"] = round(roc_auc_score(y_raw, probs) * 100, 1)

update_metrics()

# ==========================================
# UI TEMPLATE WITH IMMERSIVE CYBER TABLE
# ==========================================
html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>FraudGuard AI | Advanced Risk Engine</title>

<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'><path d='M12 22q-3.475 0-6.4-1.788T1.2 15.35q-.175-.3-.237-.625T.9 14q0-.475.175-.887t.525-.713l3.6-3.6q.3-.3.7-.463T6.75 8.175q.45 0 .863.175t.687.475l.9.9V4q0-.825.587-1.413T11.2 2h1.6q.825 0 1.413.588T14.8 4v5.725l.9-.9q.275-.275.688-.463t.862-.187q.45 0 .85.163t.7.487l3.6 3.6q.35.35.525.763t.175.912q0 .35-.062.675t-.238.625q-1.475 3.075-4.4 4.863T12 22Z'/></svg>">

<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:"Segoe UI",sans-serif;}
html{scroll-behavior:smooth;}

body{
    background-color: #050814;
    color:#fff;
    padding-bottom: 40px;
    position: relative;
    overflow-x: hidden;
}

.cyber-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: radial-gradient(circle at 50% 10%, #152244 0%, #050814 75%);
    opacity: 0.95;
}
.cyber-grid {
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient(rgba(77, 163, 255, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(77, 163, 255, 0.04) 1px, transparent 1px);
    background-size: 40px 40px;
}
.radar-beam {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, transparent, rgba(75, 108, 255, 0.25), transparent);
    animation: radarSweep 8s linear infinite;
    box-shadow: 0 0 12px rgba(77, 163, 255, 0.4);
}
@keyframes radarSweep {
    0% { top: 0%; opacity: 0; }
    5% { opacity: 1; }
    95% { opacity: 1; }
    100% { top: 100%; opacity: 0; }
}

header{
    padding:20px 60px;
    background:rgba(5, 10, 25, 0.85);
    backdrop-filter:blur(16px);
    border-bottom: 1px solid rgba(77, 163, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 10;
}
.logo{
    font-family:"Trebuchet MS","Segoe UI",sans-serif;
    font-weight:800;
    letter-spacing:1.6px;
    color:#7aa2ff;
}
.logo span{color:#4da3ff;}

.rbi-badge {
    font-size: 11px;
    background: rgba(77, 163, 255, 0.12);
    border: 1px solid rgba(77, 163, 255, 0.25);
    color: #a4c6ff;
    padding: 5px 14px;
    border-radius: 20px;
    font-weight: 600;
}

.hero{
    text-align:center;
    padding:110px 20px 50px;
    position: relative;
    z-index: 5;
}
.hero h1{
    font-size:48px;
    margin-bottom:16px;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 30%, #aec7ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p{color:#b5c3ff; margin-bottom:34px; font-size:17px;}
.hero-btn{
    display:inline-block;
    background: linear-gradient(135deg,#5e4dff,#007aff);
    padding:14px 38px;
    border-radius:30px;
    color:white;
    text-decoration:none;
    transition:.3s;
    font-weight: 600;
}
.hero-btn:hover{
    transform:translateY(-2px);
    box-shadow:0 12px 30px rgba(0, 122, 255, 0.5);
}

.section{
    display:flex;
    justify-content:center;
    padding:25px 20px;
    position: relative;
    z-index: 5;
}

.card{
    width:620px;
    background: rgba(10, 16, 36, 0.65);
    border: 1px solid rgba(77, 163, 255, 0.15);
    backdrop-filter: blur(20px);
    border-radius:24px;
    padding:36px;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
}
.card h2{text-align:center; margin-bottom:8px; font-size: 23px; font-weight: 700;}
.card p{text-align:center; color:#8fa3df; margin-bottom:26px; font-size: 14px; line-height: 1.5;}

.metrics-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 24px;
    background: rgba(0, 0, 0, 0.25);
    padding: 6px;
    border-radius: 16px;
}
.metric-box {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(77, 163, 255, 0.08);
    border-radius: 12px;
    padding: 16px 6px;
    text-align: center;
}
.metric-box .val { font-size: 21px; font-weight: 700; color: #0084ff; }
.metric-box .val.recall-color { color: #ff453a; }
.metric-box .val.auc-color { color: #30d158; }
.metric-box .lbl { font-size: 9.5px; font-weight: 600; text-transform: uppercase; color: #8fa3df; margin-top: 5px;}

.form-group { margin-bottom: 18px; text-align: left; }
.form-group label { display: block; font-size: 12px; font-weight: 600; color: #8fa3df; margin-bottom: 7px; }
input[type="number"]{
    width:100%; height: 52px; border-radius:14px; padding:0 18px;
    background: rgba(5, 8, 20, 0.7); border: 1px solid rgba(77, 163, 255, 0.2);
    color: white; font-size: 16px; transition: all 0.25s;
}
input[type="number"]:focus { outline: none; border-color: #0084ff; box-shadow: 0 0 14px rgba(0, 132, 255, 0.25); }

button{
    width:100%; margin-top:10px; padding:16px; border-radius:14px; border:none;
    background: linear-gradient(180deg, #4b6cff 0%, #0052cc 100%); color:white;
    font-weight: 600; font-size: 15px; cursor:pointer; transition: all 0.2s;
}
button:hover{ transform:translateY(-1.5px); box-shadow: 0 8px 20px rgba(75, 108, 255, 0.4); }
button.btn-smote { background: linear-gradient(180deg, #30d158 0%, #1e8737 100%); }
button.btn-smote.active { background: linear-gradient(180deg, #ff453a 0%, #c62820 100%); }

.result{
    margin-top:24px; padding:16px; border-radius:14px; text-align:center;
    font-weight: 700; font-size: 13.5px;
    animation: popIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes popIn { from { opacity: 0; transform: scale(0.96); } to { opacity: 1; transform: scale(1); } }
.spam { background: rgba(255, 69, 58, 0.1); border: 1px solid rgba(255, 69, 58, 0.3); color: #ff6961; }
.ham { background: rgba(48, 209, 88, 0.1); border: 1px solid rgba(48, 209, 88, 0.3); color: #30d158; }

/* =========================================================================
   TRUE CYBER BLENDED & ANIMATED MATRIX TABLE SYSTEM
   ========================================================================= */
.cyber-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 12px;
    margin-top: 15px;
}
.cyber-table th {
    font-size: 11px;
    text-transform: uppercase;
    color: #4da3ff;
    text-align: left;
    padding: 8px 16px;
    letter-spacing: 1.2px;
    border-bottom: 1px solid rgba(77, 163, 255, 0.2);
    text-shadow: 0 0 10px rgba(77, 163, 255, 0.4);
}

/* Translucent row containers that completely blend into the cyber-grid backdrop */
.cyber-table tbody tr {
    position: relative;
    background: rgba(8, 16, 40, 0.4);
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.cyber-table td {
    padding: 16px 16px;
    font-size: 14px;
    border-top: 1px solid rgba(77, 163, 255, 0.08);
    border-bottom: 1px solid rgba(77, 163, 255, 0.08);
    position: relative;
    overflow: hidden;
}

/* Rounded caps for structural table rows */
.cyber-table td:first-child {
    border-left: 1px solid rgba(77, 163, 255, 0.08);
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
    font-weight: 700;
}
.cyber-table td:last-child {
    border-right: 1px solid rgba(77, 163, 255, 0.08);
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
}

/* Neon Glow Outline & Breathing Text Effects for Tier Classifications */
.row-safe {
    color: #30d158 !important;
    box-shadow: inset 4px 0 0 #30d158, 0 0 15px rgba(48, 209, 88, 0.05);
    animation: textBreatheGreen 3s ease-in-out infinite;
}
.row-warning {
    color: #ffd60a !important;
    box-shadow: inset 4px 0 0 #ffd60a, 0 0 15px rgba(255, 214, 10, 0.05);
    animation: textBreatheYellow 3s ease-in-out infinite;
}
.row-danger {
    color: #ff453a !important;
    box-shadow: inset 4px 0 0 #ff453a, 0 0 15px rgba(255, 69, 58, 0.05);
    animation: textBreatheRed 3s ease-in-out infinite;
}

/* Hover glow upgrades */
.cyber-table tbody tr:hover {
    transform: translateY(-2px) scale(1.01);
    background: rgba(12, 28, 72, 0.55);
}
.cyber-table tbody tr:hover .row-safe { box-shadow: inset 4px 0 0 #30d158, 0 0 25px rgba(48, 209, 88, 0.2); }
.cyber-table tbody tr:hover .row-warning { box-shadow: inset 4px 0 0 #ffd60a, 0 0 25px rgba(255, 214, 10, 0.2); }
.cyber-table tbody tr:hover .row-danger { box-shadow: inset 4px 0 0 #ff453a, 0 0 25px rgba(255, 69, 58, 0.2); }

/* Moving Glass Laser Scan Line Overlay Effect */
.cyber-table tbody tr::after {
    content: '';
    position: absolute;
    top: 0;
    left: -150%;
    width: 50%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(77, 163, 255, 0.12), transparent);
    transform: skewX(-25deg);
    animation: rowScanLine 6s infinite ease-in-out;
}
.cyber-table tbody tr:nth-child(2)::after { animation-delay: 2s; }
.cyber-table tbody tr:nth-child(3)::after { animation-delay: 4s; }

@keyframes rowScanLine {
    0% { left: -150%; }
    30% { left: 150%; }
    100% { left: 150%; }
}

@keyframes textBreatheGreen {
    0%, 100% { text-shadow: 0 0 4px rgba(48, 209, 88, 0.2); }
    50% { text-shadow: 0 0 12px rgba(48, 209, 88, 0.7); }
}
@keyframes textBreatheYellow {
    0%, 100% { text-shadow: 0 0 4px rgba(255, 214, 10, 0.2); }
    50% { text-shadow: 0 0 12px rgba(255, 214, 10, 0.7); }
}
@keyframes textBreatheRed {
    0%, 100% { text-shadow: 0 0 4px rgba(255, 69, 58, 0.2); }
    50% { text-shadow: 0 0 12px rgba(255, 69, 58, 0.7); }
}

/* Pulsating Matrix Dot Nodes */
.cyber-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-right: 10px;
    vertical-align: middle;
}
.row-safe .cyber-dot { background: #30d158; box-shadow: 0 0 8px #30d158; }
.row-warning .cyber-dot { background: #ffd60a; box-shadow: 0 0 8px #ffd60a; }
.row-danger .cyber-dot { background: #ff453a; box-shadow: 0 0 8px #ff453a; }

.features{ padding:80px 60px 40px; text-align:center; position: relative; z-index: 5; }
.features h2{font-size:36px; margin-bottom:12px; font-weight: 700;}
.features p{color:#b5c3ff; margin-bottom:44px;}

.feature-grid{
    display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
    gap:30px; max-width: 1060px; margin: 0 auto;
}
.feature-card{
    background: rgba(14, 22, 46, 0.5); border: 1px solid rgba(77, 163, 255, 0.08);
    backdrop-filter: blur(10px); border-radius:22px; padding:44px 34px;
}
.feature-card .icon{ font-size:38px; margin-bottom:20px; display: inline-block; }

footer{
    padding:30px 22px; text-align:center; background: rgba(4, 7, 18, 0.9);
    color:#637bb3; font-size: 13px; border-top: 1px solid rgba(77, 163, 255, 0.08);
    margin-top: 60px; position: relative; z-index: 10;
}
</style>
</head>

<body>

<div class="cyber-bg">
    <div class="cyber-grid"></div>
    <div class="radar-beam"></div>
</div>

<header>
    <div class="logo">🛡️ Fraud<span>Guard</span> AI</div>
    <div class="rbi-badge">RBI Security Mandate Compliant</div>
</header>

<section class="hero">
    <h1>Credit Card Fraud Engine</h1>
    <p>Analyze transaction anomalies and evaluate class balance metrics interactively</p>
    <a href="#features" class="hero-btn">Explore Features</a>
</section>

<!-- MAIN BLOCK 1: TRANSACTION SCANNER -->
<section class="section" id="audit-section">
<div class="card">
    <h2>Transaction Risk Audit</h2>
    <p>Scan live UPI and card telemetry vectors against the fraud matrix</p>
    
    <form method="post" action="/#audit-section">
        <input type="hidden" name="action" value="predict">
        <div class="form-group">
            <label>Transaction Amount (₹)</label>
            <input type="number" step="1" name="amount" value="{{ inputs.amount if inputs else '1500' }}" required>
        </div>
        <div class="form-group">
            <label>Time of Transaction (24-Hour Index: 00 to 23)</label>
            <input type="number" min="0" max="23" name="time" value="{{ inputs.time if inputs else '14' }}" required>
        </div>
        <div class="form-group">
            <label>Device / Location Deviation Delta Score (0.0 to 10.0)</label>
            <input type="number" step="0.1" min="0" max="10" name="deviation" value="{{ inputs.deviation if inputs else '1.1' }}" required>
        </div>
        <button type="submit">Execute Risk Evaluation</button>
    </form>

    {% if prediction is not none %}
        {% if prediction == 1 %}
            <div class="result spam">🚨 CRITICAL THREAT: APPLIED POSITIVE FRICTION VIA RBI PROTOCOL</div>
        {% else %}
            <div class="result ham">✅ AUTHENTICATION CLEAR: VERIFIED LOW RISK COMPLIANCE PATTERN</div>
        {% endif %}
    {% endif %}
</div>
</section>

<!-- MAIN BLOCK 2: ENGINE TELEMETRY MATRIX -->
<section class="section" id="metrics-section">
<div class="card">
    <h2>Model Telemetry Matrix</h2>
    <p>Interactive evaluation metrics for skewed financial sets (Current N = 312)</p>

    <div class="metrics-row">
        <div class="metric-box">
            <div class="val">{{ metrics.precision }}%</div>
            <div class="lbl">Precision</div>
        </div>
        <div class="metric-box">
            <div class="val recall-color">{{ metrics.recall }}%</div>
            <div class="lbl">Recall</div>
        </div>
        <div class="metric-box">
            <div class="val auc-color">{{ metrics.roc_auc }}%</div>
            <div class="lbl">ROC-AUC</div>
        </div>
    </div>

    <form method="post" action="/#metrics-section">
        <input type="hidden" name="action" value="toggle_smote">
        {% if smote_enabled %}
            <button type="submit" class="btn-smote active">Deactivate SMOTE Optimization</button>
            <div style="color:#30d158; font-size:12.5px; margin-top:14px; text-align:center; font-weight:600;">
                ● Class Resampling Engaged: Optimized for Minority Attack Vectors
            </div>
        {% else %}
            <button type="submit" class="btn-smote">Deploy SMOTE Optimization</button>
            <div style="color:#ff453a; font-size:12.5px; margin-top:14px; text-align:center; font-weight:600;">
                ● Imbalanced Baseline Mode: Susceptible to Structural False Negatives
            </div>
        {% endif %}
    </form>
</div>
</section>

<!-- NEW BLOCK 3: FULLY CYBER-BLENDED & ANIMATED HUD RISK TABLE -->
<section class="section" id="matrix-table-section">
<div class="card" style="width:640px; background: rgba(6, 11, 28, 0.4); border-color: rgba(77, 163, 255, 0.1); box-shadow: 0 20px 40px rgba(0,0,0,0.6);">
    <h2>Telemetry Vector Range Configuration</h2>
    <p>Operational feature boundaries computed by the machine learning algorithm to group risk metrics</p>
    
    <table class="cyber-table">
        <thead>
            <tr>
                <th>Risk Tier</th>
                <th>Amount (₹)</th>
                <th>Time (24hr)</th>
                <th>Deviation Score</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="row-safe"><span class="cyber-dot"></span>SAFE</td>
                <td>₹0 - ₹10,000</td>
                <td>06:00 - 22:00</td>
                <td>0.0 - 2.0</td>
            </tr>
            <tr>
                <td class="row-warning"><span class="cyber-dot"></span>WARNING</td>
                <td>₹10,001 - ₹50,000</td>
                <td>22:01 - 00:00</td>
                <td>2.1 - 4.9</td>
            </tr>
            <tr>
                <td class="row-danger"><span class="cyber-dot"></span>CRITICAL</td>
                <td>₹50,001+</td>
                <td>00:01 - 05:59</td>
                <td>5.0 - 10.0</td>
            </tr>
        </tbody>
    </table>
</div>
</section>

<section class="features" id="features">
    <h2>Core Features</h2>
    <p>Smart. Secure. Interactive.</p>
    <div class="feature-grid">
        <div class="feature-card"><div class="icon">⚡</div><div style="margin-top:8px;">UPI & Card Telemetry Analysis</div></div>
        <div class="feature-card"><div class="icon">🧠</div><div style="margin-top:8px;">Resampling Metric Diagnostics</div></div>
        <div class="feature-card"><div class="icon">🛡️</div><div style="margin-top:8px;">Fast Sub-millisecond Inference</div></div>
    </div>
</section>

<footer>
    © 2026 FraudGuard AI Cluster | Advanced Financial Risk Architecture
</footer>

</body>
</html>
"""

# ==========================================
# ROUTE GATEWAYS
# ==========================================
@app.route("/", methods=["GET", "POST"])
def home():
    global model, smote_enabled
    prediction = None
    inputs = None

    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "predict":
            amount = float(request.form["amount"])
            time = float(request.form["time"])
            deviation = float(request.form["deviation"])
            inputs = {"amount": amount, "time": time, "deviation": deviation}
            
            sample = scaler.transform([[amount, time, deviation]])
            prediction = int(model.predict(sample)[0])

        elif action == "toggle_smote":
            smote_enabled = not smote_enabled
            if smote_enabled:
                legit_indices = np.where(y_raw == 0)[0]
                fraud_indices = np.where(y_raw == 1)[0]
                
                oversampled_fraud_indices = np.random.choice(fraud_indices, size=len(legit_indices), replace=True)
                
                X_resampled = np.vstack([X_raw[legit_indices], X_raw[oversampled_fraud_indices]])
                y_resampled = np.array([0] * len(legit_indices) + [1] * len(legit_indices))
                
                X_scaled_resampled = scaler.fit_transform(X_resampled)
                model = LogisticRegression(class_weight=None)
                model.fit(X_scaled_resampled, y_resampled)
            else:
                model = LogisticRegression(class_weight=None)
                model.fit(X_scaled, y_raw)
            
            update_metrics()

    return render_template_string(
        html, 
        prediction=prediction, 
        metrics=metrics, 
        smote_enabled=smote_enabled,
        inputs=inputs
    )

if __name__ == "__main__":
    app.run(debug=True)
    