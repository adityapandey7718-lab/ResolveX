from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)

# NEW: secret key
app.config['SECRET_KEY'] = 'secret123'

# -----------------------------
# Database Configuration
# -----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# NEW: Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -----------------------------
# NEW: User Model
# -----------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -----------------------------
# Existing Ticket Model
# -----------------------------
class Ticket(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    message = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(50))
    response = db.Column(db.Text)
    feedback = db.Column(db.String(20))

with app.app_context():
    db.create_all()

# -----------------------------
# Training Data (same)
# -----------------------------
training_data = {
    "billing": ["refund not received", "charged twice"],
    "technical": ["app crashing", "error 500"],
    "account": ["forgot password", "cannot login"],
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

knowledge_base = {
    "billing": "Please check your billing section in account settings.",
    "technical": "Try clearing cache and restarting the app.",
    "account": "Click on 'Forgot Password' to reset."
}

# -----------------------------
# NEW: Auth Routes
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data["username"]).first()

        if user and check_password_hash(user.password, data["password"]):
            login_user(user)
            return redirect("/")
        return "Invalid credentials"

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form

        hashed_password = generate_password_hash(data["password"])

        user = User(username=data["username"], password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# -----------------------------
# Routes (protected)
# -----------------------------

@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST", "GET"])
@login_required
def chat():

    if request.method == "GET":
        return redirect("/")

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid request format"}), 400

    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    prediction = model.predict([message])[0]
    intent = label_encoder.inverse_transform([prediction])[0]

    probs = model.predict_proba([message])[0]
    confidence = max(probs)

    response = knowledge_base.get(intent, "Sorry, I couldn't understand your issue.")

    ticket_id = str(uuid.uuid4())[:8]

    ticket = Ticket(
        id=ticket_id,
        message=message,
        intent=intent,
        response=response
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
@login_required
def feedback(ticket_id):

    ticket = Ticket.query.get(ticket_id)

    if not ticket:
        return jsonify({"error": "Invalid ticket ID"}), 404

    data = request.get_json()

    helpful = data.get("helpful")

    if helpful:
        ticket.feedback = "positive"
    else:
        ticket.feedback = "negative"

        texts.append(ticket.message)
        labels.append(ticket.intent)

        encoded = label_encoder.fit_transform(labels)
        model.fit(texts, encoded)

    db.session.commit()

    return jsonify({"message": "Feedback recorded"})


@app.route("/tickets")
@login_required
def get_tickets():
    tickets = Ticket.query.all()

    return jsonify([{
        "id": t.id,
        "message": t.message,
        "intent": t.intent,
        "response": t.response,
        "feedback": t.feedback
    } for t in tickets])


if __name__ == "__main__":
    app.run(debug=True)