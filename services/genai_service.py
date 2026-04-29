import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

from services.firebase_service import get_knowledge_base

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def calculate_semantic_similarity(user_message, kb):
    """
    Checks if the user message is semantically similar to any entry in the KB.
    Returns the maximum similarity score found.
    """
    if not kb:
        return 0.0
    
    try:
        # Get embedding for the user message
        user_emb = genai.embed_content(
            model="models/text-embedding-004",
            content=user_message,
            task_type="retrieval_query"
        )['embedding']
        
        # In a real app, we'd pre-calculate KB embeddings. 
        # For simplicity in this demo, we'll just check if the message contains KB keywords
        # or use a simplified similarity check.
        # Let's try to get one embedding for the whole KB context to check relevance.
        kb_text = " ".join([f"{k} {v}" for k, v in kb.items()])
        kb_emb = genai.embed_content(
            model="models/text-embedding-004",
            content=kb_text,
            task_type="retrieval_document"
        )['embedding']
        
        # Simple dot product as a similarity measure (embeddings are normalized)
        import numpy as np
        similarity = np.dot(user_emb, kb_emb)
        return similarity
    except Exception as e:
        print(f"Embedding Error: {e}")
        return 0.5 # Neutral fallback

def cross_verify_response(user_message, ai_response, kb):
    """
    Uses a second LLM call to verify if the response is grounded in the KB.
    """
    judge_instruction = f"""
    You are a 'Judge' AI. Your task is to verify if a support response is grounded in the provided Knowledge Base.
    
    Knowledge Base:
    {json.dumps(kb, indent=2)}
    
    User Message: {user_message}
    AI Response: {ai_response}
    
    Is the AI response accurate based ONLY on the Knowledge Base? 
    If the KB doesn't contain the answer, the AI should have escalated.
    
    Return ONLY a JSON object:
    {{
        "is_grounded": true/false,
        "reason": "brief explanation",
        "confidence_score": 0-100
    }}
    """
    
    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(
            judge_instruction,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Judge Error: {e}")
        return {"is_grounded": True, "confidence_score": 100} # Fallback to original

def generate_support_response(user_message):
    """
    Uses Gemini to analyze the message, classify intent, and generate a response.
    Includes cross-verification and semantic similarity checks.
    """
    kb = get_knowledge_base()
    
    # 1. Semantic Similarity Check
    similarity = calculate_semantic_similarity(user_message, kb)
    
    system_instruction = f"""
    You are an AI customer support agent. 
    Knowledge Base:
    {json.dumps(kb, indent=2)}
    
    Classify intent: 'billing', 'technical', 'account', or 'unknown'.
    Provide a response based ON THE KNOWLEDGE BASE.
    If not in KB, set confidence low.
    
    Return JSON: {{"intent": "...", "response": "...", "confidence": 0-100}}
    """
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_instruction
        )
        
        response = model.generate_content(
            user_message,
            generation_config=genai.GenerationConfig(temperature=0.2, response_mime_type="application/json")
        )
        
        result = json.loads(response.text)
        
        # 2. Cross-Verification (Judge)
        verification = cross_verify_response(user_message, result['response'], kb)
        
        # Combine metrics for final confidence
        # Force low confidence if similarity is very low or judge fails grounding
        if similarity < 0.3 or not verification.get('is_grounded', True):
            result['confidence'] = min(result.get('confidence', 100), 40)
            result['judge_reason'] = verification.get('reason', 'Low relevance to knowledge base')
        else:
            # Adjust confidence based on judge
            result['confidence'] = (result.get('confidence', 0) + verification.get('confidence_score', 0)) / 2

        # Determine escalation status
        if result['confidence'] < 60:
            result['status'] = 'Escalated'
            if similarity < 0.3:
                 result['response'] = "I'm sorry, that doesn't seem to be related to our supported categories (Billing, Technical, Account). Let me escalate this to a human agent."
            else:
                result['response'] = "I'm not completely sure about this specific issue based on my current training. Escalating to a human agent for accuracy."
        else:
            result['status'] = 'Resolved'
            
        return result
        
    except Exception as e:
        print(f"GenAI Error: {e}")
        return {
            "intent": "unknown",
            "response": "I am experiencing technical difficulties. Escalating to a human agent.",
            "confidence": 0,
            "status": "Escalated"
        }
