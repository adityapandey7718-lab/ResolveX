# Usage Guide

This guide explains how to use ResolveX from both the customer and administrator perspectives.

---

## Customer Workflow

### 1. Signup & Login
- Navigate to the homepage.
- Use the **Sign Up** page to create an account with email or use **Google Sign-In**.
- Once logged in, you will be redirected to the Chat Dashboard.

### 2. Chatting with AI
- Type your support query in the chat box (e.g., "How do I reset my password?").
- The AI will analyze your message, classify it (Billing, Technical, Account), and provide a response.
- **Confidence Scoring**: If the AI is unsure (confidence < 60%), it will automatically mark the ticket as "Escalated" for human review.

### 3. Providing Feedback (The Learning Step)
- Below each AI response, you will see "Helpful?" (Thumbs up/down).
- If you click **No (Thumbs Down)**:
    - An optional form appears.
    - Provide the **correct solution** and the **category**.
    - This feedback is critical as it helps the system learn.

---

## Admin Workflow

### 1. Accessing the Dashboard
- Navigate to `/admin`.
- You will see high-level statistics:
    - Total tickets.
    - Intent breakdown (Billing, Technical, Account).
    - Feedback sentiment (Positive vs Negative).
    - Escalation count.

### 2. Reviewing Tickets
- The ticket table shows all user interactions.
- Tickets marked as **Escalated** (red badge) should be prioritized.
- Click on a ticket to view the full conversation and user feedback.

### 3. Promoting to Knowledge Base (KB)
- If a user has provided a high-quality "Correct Answer" in their negative feedback:
    - Review the answer for accuracy.
    - Click the **"Promote to KB"** button.
    - This action immediately updates the underlying knowledge base, and the AI will use this new information for all future similar queries.

### 4. Manual Ticket Updates
- Admins can manually override a ticket's status (e.g., changing from "Escalated" to "Resolved") or update the response shown to the user.

---

## Best Practices for Queries
- **Be Specific**: Instead of "It's broken," try "The login page shows a 404 error."
- **One Topic at a Time**: The AI performs best when addressing one clear issue per message.
- **Provide Context**: If you have a ticket ID from a previous interaction, include it if prompted.
