from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os, json, uuid, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
DATA_FILE = os.path.join(BASE_DIR, "chemicals.json")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'lab.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class History(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    chem_a = db.Column(db.String(50), nullable=False)
    chem_b = db.Column(db.String(50), nullable=False)
    result = db.Column(db.String(200))
    description = db.Column(db.String(500))
    safety = db.Column(db.String(200))
    color = db.Column(db.String(50))
    animation = db.Column(db.String(100))
    time = db.Column(db.String(50))

with app.app_context():
    db.create_all()

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route("/api/chemicals")
def api_chemicals():
    data = load_data()
    return jsonify(data["chemicals"])

@app.route("/api/mix", methods=["POST"])
def api_mix():
    payload = request.get_json(force=True)
    user = (payload.get("user") or "Guest").strip() or "Guest"
    a = payload.get("chemA")
    b = payload.get("chemB")
    t = datetime.datetime.utcnow().isoformat() + "Z"

    data = load_data()
    key = f"{a}+{b}"
    rkey = f"{b}+{a}"
    reaction = data.get("reactions", {}).get(key) or data.get("reactions", {}).get(rkey) or {
        "reaction": "No visible reaction",
        "description": "No noticeable change observed.",
        "safety": "No special hazard noted for dilute mixture.",
        "color": "",
        "animation": ""
    }

    rec = History(
        id=uuid.uuid4().hex[:10],
        user=user,
        chem_a=a,
        chem_b=b,
        result=reaction["reaction"],
        description=reaction.get("description",""),
        safety=reaction.get("safety",""),
        color=reaction.get("color",""),
        animation=reaction.get("animation",""),
        time=t
    )
    db.session.add(rec)
    db.session.commit()

    return jsonify({"ok": True, "id": rec.id})

@app.route("/api/history")
def api_history():
    history = History.query.order_by(History.time.desc()).all()
    results = []
    for h in history:
        results.append({
            "id": h.id,
            "user": h.user,
            "chemicals": [h.chem_a, h.chem_b],
            "result": h.result,
            "description": h.description,
            "safety": h.safety,
            "color": h.color,
            "animation": h.animation,
            "time": h.time
        })
    return jsonify(results)

@app.route("/api/result/<rid>")
def api_result(rid):
    h = History.query.get(rid)
    if h:
        return jsonify({
            "id": h.id,
            "user": h.user,
            "chemicals": [h.chem_a, h.chem_b],
            "result": h.result,
            "description": h.description,
            "safety": h.safety,
            "color": h.color,
            "animation": h.animation,
            "time": h.time
        })
    return jsonify({"error": "not found"}), 404
@app.route("/test")
def test_db():
    h = History.query.all()
    return "<br>".join([f"{x.user} {x.chem_a}+{x.chem_b} -> {x.result}" for x in h])

if __name__ == "__main__":
    app.run(debug=True)
