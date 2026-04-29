import os
from services.firebase_service import update_knowledge_base_entry

# Update Billing
update_knowledge_base_entry(
    "billing", 
    "ResolveX is not a bank and cannot process refunds directly. If you have a billing dispute or need a refund, please contact your bank or card issuer. For ResolveX subscription management, go to Settings > Billing."
)

# Update Technical
update_knowledge_base_entry(
    "technical",
    "To resolve most technical issues: 1. Clear your browser cache. 2. Restart the application. 3. Ensure you are on the latest version. If the error persists, please provide the specific error code you are seeing."
)

# Update Account
update_knowledge_base_entry(
    "account",
    "To manage your account: 1. Visit the Profile section to change your email or password. 2. For security, enable Two-Factor Authentication in Settings > Security. If you are locked out, use the 'Forgot Password' link."
)

print("KNOWLEDGE BASE UPDATED WITH NEW POLICIES")
