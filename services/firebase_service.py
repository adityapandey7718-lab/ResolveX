import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    # Explicitly set project ID to avoid mismatch errors
    project_id = os.getenv("FIREBASE_PROJECT_ID")
    firebase_admin.initialize_app(cred, {
        'projectId': project_id
    })

db = firestore.client()

def verify_token(id_token):
    """Verifies the Firebase ID token and returns the decoded token."""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        error_msg = str(e)
        # Handle Clock Skew: "Token used too early"
        if "Token used too early" in error_msg:
            import time
            for i in range(3):  # Try up to 3 times
                print(f"DEBUG: Clock skew detected (Attempt {i+1}). Retrying in 2 seconds...")
                time.sleep(2.0)
                try:
                    return auth.verify_id_token(id_token)
                except Exception as retry_e:
                    error_msg = str(retry_e)
                    if "Token used too early" not in error_msg:
                        break
        
        print(f"DEBUG: Firebase Token Verification Failed. Error: {error_msg}")
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

def save_ticket(ticket_data):
    """Saves or updates a ticket in Firestore."""
    doc_ref = db.collection('tickets').document(ticket_data['id'])
    doc_ref.set(ticket_data, merge=True)

def get_ticket(ticket_id):
    """Retrieves a specific ticket by ID."""
    doc = db.collection('tickets').document(ticket_id).get()
    return doc.to_dict() if doc.exists else None

def add_message_to_ticket(ticket_id, role, content):
    """Appends a message to the conversation history of a ticket."""
    doc_ref = db.collection('tickets').document(ticket_id)
    doc_ref.update({
        'messages': firestore.ArrayUnion([{'role': role, 'content': content}])
    })

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

def update_ticket_feedback(ticket_id, feedback, correct_answer=None, correct_category=None):
    """Updates the feedback on a ticket with optional user-provided corrections."""
    doc_ref = db.collection('tickets').document(ticket_id)
    update_data = {'feedback': feedback}
    if correct_answer:
        update_data['correct_answer'] = correct_answer
    if correct_category:
        update_data['correct_category'] = correct_category
    
    doc_ref.update(update_data)

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

def delete_ticket(ticket_id):
    """Deletes a ticket from Firestore."""
    db.collection('tickets').document(ticket_id).delete()

