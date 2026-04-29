import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

from services.firebase_service import get_knowledge_base

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("WARNING: GOOGLE_API_KEY not found in environment!")
genai.configure(api_key=api_key)

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
            model="models/gemini-embedding-001",
            content=user_message,
            task_type="retrieval_query"
        )['embedding']
        
        # In a real app, we'd pre-calculate KB embeddings. 
        # For simplicity in this demo, we'll just check if the message contains KB keywords
        # or use a simplified similarity check.
        # Let's try to get one embedding for the whole KB context to check relevance.
        kb_text = " ".join([f"{k} {v}" for k, v in kb.items()])
        kb_emb = genai.embed_content(
            model="models/gemini-embedding-001",
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
    Second-pass verification (Judge model) to check if the AI response 
    is actually supported by the knowledge base.
    """
    kb_context = json.dumps(kb, indent=2)
    
    judge_instruction = f"""
    You are a fact-checker for a customer support AI.
    Knowledge Base: {kb_context}
    
    User asked: {user_message}
    AI responded: {ai_response}
    
    Task: Is the AI's response supported by the Knowledge Base? 
    Return ONLY a JSON object:
    {{"is_grounded": true/false, "confidence_score": 0-100, "reason": "..."}}
    """
    
    try:
        model = genai.GenerativeModel("gemini-flash-lite-latest")
        response = model.generate_content(judge_instruction)
        
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        print(f"Judge Error: {e}")
        return {"is_grounded": True, "confidence_score": 100} # Fallback to original

def generate_support_response(user_message, chat_history=None):
    """
    Uses Gemini to analyze the message, classify intent, and generate a response.
    Includes chat history for conversational context.
    """
    kb = get_knowledge_base()
    
    # 1. Semantic Similarity Check
    similarity = calculate_semantic_similarity(user_message, kb)
    
    history_context = ""
    if chat_history:
        history_context = "Conversation History:\n" + "\n".join([f"{m['role']}: {m['content']}" for m in chat_history])
    
    system_instruction = f"""
    You are an AI customer support agent for ResolveX. 
    Knowledge Base:
    {json.dumps(kb, indent=2)}
    
    {history_context}
    
    Current User Message: {user_message}
    
    Role & Policies:
    1. YOUR ROLE: You guide users with TAILORED, STEP-BY-STEP PROCEDURES for Billing, Technical, and Account issues.
    2. BE DYNAMIC: Do not just repeat the Knowledge Base word-for-word. Use the information in the KB to construct a response that specifically addresses the user's current message and history.
    3. REFUND POLICY: ResolveX is NOT a bank. If a user asks for a refund, you MUST inform them to contact their bank directly for refund processing. You cannot process refunds.
    4. GATHER INFORMATION: If a user's initial message is vague or lacks detail (especially for Billing), you MUST ask clarifying questions (e.g., "What happened exactly?", "When did this occur?") before providing a final solution.
    5. KNOWLEDGE BASE: Use the provided KB as your primary source of truth. If information is missing, provide general guidance and maintain a professional tone.
    
    Response Format:
    Return ONLY a JSON object:
    {{"intent": "billing|technical|account|unknown", "response": "Your response here", "confidence": 0-100}}
    """
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-lite-latest",
            system_instruction=system_instruction
        )
        
        # Format history for Gemini
        formatted_history = []
        if history:
            for msg in history:
                role = "user" if msg['role'] == 'user' else "model"
                formatted_history.append({"role": role, "parts": [msg['content']]})
        
        chat = model.start_chat(history=formatted_history)
        
        response = chat.send_message(
            user_message,
            generation_config=genai.GenerationConfig(temperature=0.5)
        )
        
        # Robust JSON parsing
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        try:
            result = json.loads(text)
        except:
            # Fallback if model fails JSON
            result = {
                "intent": "unknown",
                "response": text,
                "confidence": 70
            }
        
        # 2. Cross-Verification (Judge) - Optional/Safe
        try:
            verification = cross_verify_response(user_message, result['response'], kb)
            if similarity < 0.3 or not verification.get('is_grounded', True):
                result['confidence'] = min(result.get('confidence', 100), 40)
            else:
                result['confidence'] = (result.get('confidence', 0) + verification.get('confidence_score', 0)) / 2
        except:
            print("Warning: Cross-verification failed, skipping...")

        # Determine escalation status
        if result.get('confidence', 0) < 60:
            result['status'] = 'Escalated'
        else:
            result['status'] = 'Resolved'
            
        return result
        
    except Exception as e:
        print(f"GenAI Critical Error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "intent": "unknown",
            "response": "I am experiencing technical difficulties. Let me escalate this to a human agent.",
            "confidence": 0,
            "status": "Escalated"
        }
