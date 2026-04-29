import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

from services.firebase_service import get_knowledge_base

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_support_response(user_message):
    """
    Uses Gemini to analyze the message, classify intent, and generate a response based on the knowledge base.
    Returns a dict with: intent, response, confidence, status
    """
    # Fetch dynamic knowledge base from Firestore
    kb = get_knowledge_base()
    
    system_instruction = f"""
    You are an AI customer support agent. 
    You have the following knowledge base:
    {json.dumps(kb, indent=2)}
    
    Respond to the user's message.
    You must classify the intent into one of: 'billing', 'technical', 'account', or 'unknown'.
    If the answer can be derived from the knowledge base, provide a helpful response and set confidence high (80-100).
    If the answer is NOT in the knowledge base, or you are unsure, set confidence low (0-59).
    
    Return ONLY a raw JSON object with the following schema:
    {{
        "intent": "classified_intent",
        "response": "your generated response to the user",
        "confidence": 85
    }}
    Do not use markdown code blocks like ```json ... ```, just output the raw JSON text.
    """
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_instruction
        )
        
        # Generation config to encourage JSON output
        generation_config = genai.GenerationConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
        
        response = model.generate_content(
            user_message,
            generation_config=generation_config
        )
        
        result = json.loads(response.text)
        
        confidence = result.get('confidence', 0)
        
        # Determine escalation status
        if confidence < 60:
            result['status'] = 'Escalated'
            result['response'] = "I'm not completely sure how to resolve this. Let me escalate this to a human agent who will assist you shortly."
        else:
            result['status'] = 'Resolved'
            
        return result
        
    except Exception as e:
        print(f"GenAI Error: {e}")
        # Fallback response if GenAI fails
        return {
            "intent": "unknown",
            "response": "I am experiencing technical difficulties. Escalating to a human agent.",
            "confidence": 0,
            "status": "Escalated"
        }
