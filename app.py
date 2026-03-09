from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import uuid

app = Flask(__name__)

# -----------------------------
# Database Configuration
# -----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# Database Model
# -----------------------------
class Ticket(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    message = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(50))
    response = db.Column(db.Text)
    confidence = db.Column(db.Float)
    feedback = db.Column(db.String(20))

with app.app_context():
    db.create_all()

# -----------------------------
# Training Data
# -----------------------------
training_data = {
    "billing": [
        "refund not received",
        "charged twice",
        "payment problem"
    ],
    "technical": [
        "app crashing",
        "error 500",
        "website not loading"
    ],
    "account": [
        "forgot password",
        "cannot login",
        "reset password"
    ]
}

texts = []
labels = []

for intent, samples in training_data.items():
    for s in samples:
        texts.append(s)
        labels.append(intent)

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("svc", SVC(probability=True))
])

model.fit(texts, encoded_labels)

# -----------------------------
# Knowledge Base
# -----------------------------
knowledge_base = {
    "billing": "Please check your billing section in account settings.",
    "technical": "Try clearing cache and restarting the app.",
    "account": "Click on 'Forgot Password' to reset."
}

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST", "GET"])
def chat():

    if request.method == "GET":
        return redirect("/")

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid request format"}), 400

    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # ML Prediction
    probs = model.predict_proba([message])[0]
    confidence = max(probs)

    prediction = model.predict([message])[0]
    intent = label_encoder.inverse_transform([prediction])[0]

    response = knowledge_base.get(intent, "Sorry, I couldn't understand your issue.")

    ticket_id = str(uuid.uuid4())[:8]

    ticket = Ticket(
        id=ticket_id,
        message=message,
        intent=intent,
        response=response,
        confidence=confidence
    )

    db.session.add(ticket)
    db.session.commit()

    return jsonify({
        "ticket_id": ticket_id,
        "intent": intent,
        "response": response,
        "confidence": round(confidence * 100, 2)
    })


@app.route("/feedback/<ticket_id>", methods=["POST"])
def feedback(ticket_id):

    ticket = Ticket.query.get(ticket_id)

    if not ticket:
        return jsonify({"error": "Invalid ticket ID"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request format"}), 400

    helpful = data.get("helpful")

    if helpful:
        ticket.feedback = "positive"
    else:
        ticket.feedback = "negative"

        # Retrain model
        texts.append(ticket.message)
        labels.append(ticket.intent)

        encoded = label_encoder.fit_transform(labels)
        model.fit(texts, encoded)

    db.session.commit()

    return jsonify({"message": "Feedback recorded"})


@app.route("/tickets")
def get_tickets():

    tickets = Ticket.query.all()

    result = []

    for t in tickets:
        result.append({
            "id": t.id,
            "message": t.message,
            "intent": t.intent,
            "response": t.response,
            "confidence": round(t.confidence * 100, 2) if t.confidence else None,
            "feedback": t.feedback
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)