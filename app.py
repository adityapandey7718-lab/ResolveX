from flask import Flask, request, jsonify, render_template, redirect
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


@app.route("/chat", methods=["POST", "GET"])
def chat():
    """Process user message and classify intent using ML model.

    - Redirects GET requests to the homepage to avoid browser errors.
    - Uses silent JSON parsing to prevent BadRequest exceptions.
    """
    try:
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
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/feedback/<ticket_id>", methods=["POST"])
def feedback(ticket_id):
    """Record user feedback and improve model based on corrections."""
    try:
        if ticket_id not in tickets:
            return jsonify({"error": "Invalid ticket ID"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request format"}), 400
        
        helpful = data.get("helpful")

        # If feedback is negative, retrain model with correct intent
        if helpful is False:
            message = tickets[ticket_id]["message"]
            correct_intent = data.get("correct_intent")
            
            if not correct_intent:
                return jsonify({"error": "Correct intent is required for negative feedback"}), 400
            
            # Add corrected data to training set
            texts.append(message)
            labels.append(correct_intent)
            
            # Retrain model with updated data
            encoded = label_encoder.fit_transform(labels)
            model.fit(texts, encoded)
            
            # Update ticket with correct intent
            tickets[ticket_id]["intent"] = correct_intent
            
            return jsonify({"message": "Feedback recorded. Model updated!"})
        
        return jsonify({"message": "Feedback recorded. Thank you!"})
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)