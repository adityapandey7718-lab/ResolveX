import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def verify_token(id_token):
    """Verifies the Firebase ID token and returns the decoded token."""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None

def save_ticket(ticket_data):
    """Saves a new ticket to Firestore."""
    # ticket_data should contain: id, user_id, message, intent, response, status, confidence
    doc_ref = db.collection('tickets').document(ticket_data['id'])
    doc_ref.set(ticket_data)

def get_user_tickets(user_id):
    """Retrieves tickets for a specific user."""
    tickets_ref = db.collection('tickets')
    query = tickets_ref.where(filter=firestore.FieldFilter("user_id", "==", user_id)).stream()
    return [doc.to_dict() for doc in query]

def get_all_tickets():
    """Retrieves all tickets (for admin dashboard)."""
    tickets = []
    for doc in db.collection('tickets').stream():
        tickets.append(doc.to_dict())
    return tickets

def update_ticket_feedback(ticket_id, feedback):
    """Updates the feedback on a ticket."""
    doc_ref = db.collection('tickets').document(ticket_id)
    doc_ref.update({'feedback': feedback})

def get_knowledge_base():
    """Retrieves all entries from the knowledge base."""
    kb_ref = db.collection('knowledge_base')
    docs = kb_ref.stream()
    kb = {}
    for doc in docs:
        data = doc.to_dict()
        kb[data['intent']] = data['response']
    return kb

def update_knowledge_base_entry(intent, response):
    """Updates or adds a knowledge base entry."""
    doc_ref = db.collection('knowledge_base').document(intent)
    doc_ref.set({
        'intent': intent,
        'response': response
    })

def get_ticket_stats():
    """Returns basic stats for the admin dashboard."""
    # Note: In a large production app, you'd use aggregation queries.
    # For this scale, we fetch all and count.
    tickets = get_all_tickets()
    total = len(tickets)
    billing = sum(1 for t in tickets if t.get('intent') == 'billing')
    technical = sum(1 for t in tickets if t.get('intent') == 'technical')
    account = sum(1 for t in tickets if t.get('intent') == 'account')
    positive = sum(1 for t in tickets if t.get('feedback') == 'positive')
    negative = sum(1 for t in tickets if t.get('feedback') == 'negative')
    escalated = sum(1 for t in tickets if t.get('status') == 'Escalated')
    
    return {
        "total": total,
        "billing": billing,
        "technical": technical,
        "account": account,
        "positive": positive,
        "negative": negative,
        "escalated": escalated
    }
