from flask import Flask, request, jsonify, render_template, redirect, session, url_for
from functools import wraps
import uuid
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
print("DEBUG: Environment variables loaded from .env")

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
    if decoded_token and "error" not in decoded_token:
        # Set Flask session
        session.permanent = True
        session['user_id'] = decoded_token['uid']
        session['email'] = decoded_token.get('email', '')
        return jsonify({"success": True, "message": "Authenticated"})
    else:
        error_msg = decoded_token.get("error", "Invalid token") if decoded_token else "Invalid token"
        return jsonify({"error": error_msg}), 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/signup")
def signup():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    firebase_config = {
        "apiKey": os.getenv("FIREBASE_API_KEY", ""),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": os.getenv("FIREBASE_PROJECT_ID", ""),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId": os.getenv("FIREBASE_APP_ID", "")
    }
    return render_template("signup.html", firebase_config=firebase_config)

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
    ticket_id = data.get("ticket_id")
    
    if not message:
        return jsonify({"error": "Message is required"}), 400

    user_id = session.get('user_id')
    history = []
    
    if ticket_id:
        from services.firebase_service import get_ticket
        ticket = get_ticket(ticket_id)
        if ticket and ticket.get('user_id') == user_id:
            history = ticket.get('messages', [])
    # Manage Conversational Memory
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    chat_history = session['chat_history'][-4:] # Keep last 4 messages for context

    # Process with GenAI
    ai_result = generate_support_response(message, chat_history=chat_history)
    
    # Update History
    session['chat_history'].append({"role": "user", "content": message})
    session['chat_history'].append({"role": "assistant", "content": ai_result['response']})
    session.modified = True

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

@app.route("/api/ticket/<ticket_id>")
@login_required
def get_ticket_details(ticket_id):
    from services.firebase_service import get_ticket
    user_id = session.get('user_id')
    ticket = get_ticket(ticket_id)
    
    if not ticket or ticket.get('user_id') != user_id:
        return jsonify({"error": "Ticket not found"}), 404
        
    return jsonify(ticket)

@app.route("/feedback/<ticket_id>", methods=["POST"])
@login_required
def feedback(ticket_id):
    data = request.get_json()
    helpful = data.get("helpful")
    correct_answer = data.get("correct_answer")
    correct_category = data.get("correct_category")
    feedback_value = "positive" if helpful else "negative"

    # Update in Firestore
    try:
        update_ticket_feedback(ticket_id, feedback_value, correct_answer, correct_category)
        return jsonify({"message": "Feedback recorded"})
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return jsonify({"error": "Failed to save feedback"}), 500

@app.route("/my-tickets")
@login_required
def my_tickets():
    user_id = session.get('user_id')
    tickets = get_user_tickets(user_id)
    
    # Return JSON if requested by the sidebar
    if request.args.get('json'):
        return jsonify(tickets)
        
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

@app.route("/api/admin/ticket/<ticket_id>", methods=["POST"])
@login_required
def admin_update_ticket(ticket_id):
    # In a real app, check if user is admin
    data = request.get_json()
    status = data.get("status")
    response_text = data.get("response")
    
    try:
        from services.firebase_service import db
        doc_ref = db.collection('tickets').document(ticket_id)
        update_data = {}
        if status: update_data['status'] = status
        if response_text: update_data['response'] = response_text
        
        doc_ref.update(update_data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/admin/kb", methods=["POST"])
@login_required
def admin_update_kb():
    data = request.get_json()
    intent = data.get("intent")
    response_text = data.get("response")
    
    if not intent or not response_text:
        return jsonify({"error": "Intent and response are required"}), 400
        
    try:
        from services.firebase_service import update_knowledge_base_entry
        update_knowledge_base_entry(intent, response_text)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)