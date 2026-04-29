# ResolveX - Conversational AI Support System

![ResolveX](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/Python-3.13-green)
![Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-purple)
![Firestore](https://img.shields.io/badge/DB-Firestore-orange)

ResolveX is a state-of-the-art, conversational AI customer support system. It leverages **Google Gemini** for intelligent, multi-turn dialogues and **Firebase Firestore** for persistent thread management. The system is designed to guide users through complex billing, technical, and account issues while learning and improving from every interaction.

## 🌟 Key Features

- **💬 Multi-Turn Conversations**: Maintains full context of the support session, allowing for follow-up questions and continuous problem-solving.
- **🤖 Powered by Gemini**: Uses `gemini-flash-lite-latest` for fast, intelligent, and grounded responses.
- **📚 Dynamic Knowledge Base**: All AI responses are grounded in a custom Knowledge Base stored in Firestore, ensuring accuracy and brand consistency.
- **🛡️ Fact-Checking (Judge AI)**: A secondary AI layer verifies responses against the Knowledge Base to prevent hallucinations and ensure grounding.
- **📊 Admin Dashboard**: High-level analytics on ticket volume, escalation rates, and user feedback (Positive/Negative).
- **🔄 Human-in-the-Loop Learning**: Admins can review negative feedback and update the Knowledge Base directly from the dashboard to improve future responses.
- **📂 Persistent Chat History**: Users can resume any of their previous conversations from a dedicated sidebar.
- **🌓 Adaptive Theming**: Fully responsive UI with a sleek Dark Mode.

## 📋 Supported Support Domains

| Category | Role | Policy |
|----------|------|--------|
| **💳 Billing** | Guidance & Information | ResolveX is NOT a bank. Users are guided to contact their bank for refunds. |
| **🔧 Technical** | Troubleshooting | Step-by-step procedures for app errors, bugs, and connectivity issues. |
| **👤 Account** | Security & Profile | Guidance on password resets, 2FA, and profile management. |

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Firebase Project (Firestore & Auth enabled)
- Google AI Studio API Key (Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/adityapandey7718-lab/ResolveX.git
   cd ResolveX
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key
   FIREBASE_CREDENTIALS_PATH=firebase_credentials.json
   FIREBASE_PROJECT_ID=your_project_id
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI/ML**: Google Generative AI (Gemini 1.5/3.0), NumPy (Semantic Similarity)
- **Database**: Google Cloud Firestore (NoSQL)
- **Authentication**: Firebase Authentication
- **Frontend**: HTML5, Vanilla CSS, JavaScript (ES6)
- **Charts**: Chart.js

## 🔄 The Learning Loop

1. **Interaction**: User chats with Gemini about a problem.
2. **Verification**: The "Judge" AI checks if the response matches the Knowledge Base.
3. **Feedback**: The user rates the response (👍/👎).
4. **Correction**: If negative, the user provides the correct answer/category.
5. **Improvement**: Admins review corrections and update the KB with one click, immediately improving the AI for all future users.

## 📄 License
This project is provided for educational and commercial support automation purposes.

---
**ResolveX**: Intelligent support, resolved at the speed of thought.
