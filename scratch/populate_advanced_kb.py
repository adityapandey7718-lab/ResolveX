import os
import sys

# Ensure the root directory is in the path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.firebase_service import update_knowledge_base_entry

def populate_kb():
    policies = {
        # --- BILLING ---
        "billing_general": "ResolveX subscription management can be found in Settings > Billing. We accept all major credit cards and PayPal.",
        "billing_refunds": "REFUND POLICY: ResolveX is not a bank and cannot process refunds directly. If you have a billing dispute or need a refund, you MUST contact your bank or card issuer to initiate the process.",
        "billing_failed_payment": "If your payment failed: 1. Check if your card has expired. 2. Verify that your billing address matches your bank records. 3. Ensure you have sufficient funds. 4. Contact your bank to see if they are blocking international transactions.",
        "billing_invoice": "To download invoices: Go to Dashboard > Settings > Billing History. You can download PDF receipts for all past transactions there.",
        "billing_upgrade": "To change your plan: Navigate to Settings > Subscription. Choose your new plan and click 'Update'. Changes are applied immediately and prorated.",

        # --- TECHNICAL ---
        "tech_loading_issues": "If the page isn't loading: 1. Check your internet connection. 2. Try opening ResolveX in an Incognito/Private window. 3. If it works in Incognito, clear your browser cache and cookies.",
        "tech_white_screen": "If you see a white screen after logging in: 1. Refresh the page (Ctrl+R or Cmd+R). 2. Logout and log back in. 3. Ensure your browser is up to date. Chrome or Firefox are recommended.",
        "tech_error_codes": "If you see an error code (e.g., ERR_500): Please take a screenshot and note the exact time. This usually indicates a temporary server issue. Try again in 5 minutes.",
        "tech_mobile": "ResolveX is optimized for mobile browsers. For the best experience, use Safari on iOS or Chrome on Android. We do not have a standalone app yet.",

        # --- ACCOUNT ---
        "acc_forgot_password": "If you forgot your password: Click 'Forgot Password' on the login screen. Enter your email, and we will send you a reset link. Check your Spam folder if you don't see it within 2 minutes.",
        "acc_verification": "Email Verification: If you didn't receive your verification link, go to Profile Settings and click 'Resend Verification'. Ensure your email is spelled correctly.",
        "acc_security_2fa": "Two-Factor Authentication (2FA): You can enable 2FA in Settings > Security using any TOTP app like Google Authenticator or Authy.",
        "acc_delete_account": "To delete your account: Go to Settings > Privacy > Delete Account. Warning: This action is permanent and will delete all your tickets and history. We cannot recover deleted data.",
        "acc_profile_update": "To change your name or profile picture: Go to the 'Profile' tab in the sidebar. Click 'Edit', make your changes, and hit 'Save'."
    }

    print("Populating Advanced Knowledge Base...")
    for intent, response in policies.items():
        try:
            update_knowledge_base_entry(intent, response)
            print(f"  [+] Added: {intent}")
        except Exception as e:
            print(f"  [!] Failed to add {intent}: {e}")

    print("\nSUCCESS: Knowledge Base is now broader and more detailed!")

if __name__ == "__main__":
    populate_kb()
