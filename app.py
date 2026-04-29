from flask import Flask, request, jsonify, render_template, redirect, session, url_for
from functools import wraps
import uuid
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

from services.firebase_service import verify_token, save_ticket, get_user_tickets, get_all_tickets, update_ticket_feedback, get_ticket_stats
from services.genai_service import generate_support_response

app = Flask(__name__)
# In production, set this in .env
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'development_secret_key_123')

# -----------------------------
# Auth Decorator
# -----------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------
# Auth Routes
# -----------------------------
@app.route("/login")
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    # Pass Firebase config to frontend for Google Sign-In
    firebase_config = {
        "apiKey": os.getenv("FIREBASE_API_KEY", ""),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": os.getenv("FIREBASE_PROJECT_ID", ""),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId": os.getenv("FIREBASE_APP_ID", "")
    }
    response = render_template("login.html", firebase_config=firebase_config)
    # Prevent browser from caching the login page
    return response, 200, {
        'Cache-Control': 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0',
        'Pragma': 'no-cache',
        'Expires': '-1'
    }

@app.route("/api/auth/verify", methods=["POST"])
def verify_auth():
    """Endpoint for frontend to send Firebase ID token"""
    data = request.get_json()
    id_token = data.get("idToken")
    
    if not id_token:
        return jsonify({"error": "No token provided"}), 400
        
    decoded_token = verify_token(id_token)
    if decoded_token:
        # Set Flask session
        session.permanent = True
        session['user_id'] = decoded_token['uid']
        session['email'] = decoded_token.get('email', '')
        return jsonify({"success": True, "message": "Authenticated"})
    else:
        return jsonify({"error": "Invalid token"}), 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/signup")
def signup():
    return redirect(url_for('login'))

# -----------------------------
# Main Routes
# -----------------------------
@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request format"}), 400

    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Process with GenAI
    ai_result = generate_support_response(message)
    
    ticket_id = str(uuid.uuid4())[:8]
    user_id = session.get('user_id')

    ticket_data = {
        "id": ticket_id,
        "user_id": user_id,
        "message": message,
        "intent": ai_result['intent'],
        "response": ai_result['response'],
        "confidence": ai_result['confidence'],
        "status": ai_result['status'],
        "feedback": None
    }

    # Save to Firestore
    save_ticket(ticket_data)

    return jsonify({
        "ticket_id": ticket_id,
        "intent": ai_result['intent'],
        "response": ai_result['response'],
        "confidence": ai_result['confidence'],
        "status": ai_result['status']
    })

@app.route("/feedback/<ticket_id>", methods=["POST"])
@login_required
def feedback(ticket_id):
    data = request.get_json()
    helpful = data.get("helpful")
    feedback_value = "positive" if helpful else "negative"

    # Update in Firestore
    try:
        update_ticket_feedback(ticket_id, feedback_value)
        return jsonify({"message": "Feedback recorded"})
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return jsonify({"error": "Failed to save feedback"}), 500

@app.route("/my-tickets")
@login_required
def my_tickets():
    user_id = session.get('user_id')
    tickets = get_user_tickets(user_id)
    return render_template("my_tickets.html", tickets=tickets)

# -----------------------------
# Admin Dashboard
# -----------------------------
@app.route("/admin")
@login_required
def admin():
    # Fetch tickets and stats from Firestore
    tickets = get_all_tickets()
    stats = get_ticket_stats()

    return render_template(
        "admin.html",
        tickets=tickets,
        total=stats['total'],
        billing=stats['billing'],
        technical=stats['technical'],
        account=stats['account'],
        positive=stats['positive'],
        negative=stats['negative'],
        escalated=stats['escalated']
    )

if __name__ == "__main__":
    app.run(debug=True)