import os
from services.firebase_service import get_knowledge_base

kb = get_knowledge_base()
print("KNOWLEDGE BASE ENTRIES:")
for intent, response in kb.items():
    print(f"[{intent}]: {response}")
if not kb:
    print("NO ENTRIES FOUND")
