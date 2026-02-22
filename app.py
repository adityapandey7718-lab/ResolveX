from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import uuid

app = Flask(__name__)

# -----------------------------
# Basic Training Data
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

# -----------------------------
# Knowledge Base
# -----------------------------
knowledge_base = {
    "billing": "Please check your billing section in account settings.",
    "technical": "Try clearing cache and restarting the app.",
    "account": "Click on 'Forgot Password' to reset."
}

# Store tickets temporarily
tickets = {}

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    if message.strip() == "":
        return jsonify({"error": "Message is required"}), 400

    prediction = model.predict([message])[0]
    intent = label_encoder.inverse_transform([prediction])[0]

    response = knowledge_base.get(intent, "Sorry, I couldn't understand your issue.")

    ticket_id = str(uuid.uuid4())[:8]

    tickets[ticket_id] = {
        "message": message,
        "intent": intent
    }

    return jsonify({
        "ticket_id": ticket_id,
        "intent": intent,
        "response": response
    })


@app.route("/feedback/<ticket_id>", methods=["POST"])
def feedback(ticket_id):
    data = request.get_json()
    helpful = data.get("helpful")

    if ticket_id not in tickets:
        return jsonify({"error": "Invalid ticket ID"}), 404

    # If feedback is negative, retrain model
    if helpful is False:
        message = tickets[ticket_id]["message"]
        correct_intent = tickets[ticket_id]["intent"]

        texts.append(message)
        labels.append(correct_intent)

        encoded = label_encoder.fit_transform(labels)
        model.fit(texts, encoded)

    return jsonify({"message": "Feedback recorded. Model updated!"})


if __name__ == "__main__":
    app.run(debug=True)