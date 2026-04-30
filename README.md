# ResolveX: Intelligent AI Support with Learning Feedback Loops

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/yourusername/ResolveX)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-yellow.svg)](https://flask.palletsprojects.com/)
[![Firebase](https://img.shields.io/badge/Firebase-Auth%20%26%20Firestore-orange.svg)](https://firebase.google.com/)
[![AI](https://img.shields.io/badge/Gemini-Flash--Latest-red.svg)](https://aistudio.google.com/)

**ResolveX** is a next-generation customer support automation platform that doesn't just answer questions—it learns from them. Built for speed, accuracy, and continuous improvement, ResolveX bridges the gap between AI automation and human expertise through a unique learning feedback loop.

---

## 📖 Problem Statement
Traditional chatbots often fail because they are static; once they encounter an edge case or a new type of query, they provide generic "I don't know" responses or hallucinate incorrect information. Businesses need a system that can be updated in real-time by human agents without requiring code changes or expensive model fine-tuning.

## 🚀 Why ResolveX?
- **Self-Improving**: Captures unresolved queries and user corrections to expand its Knowledge Base dynamically.
- **Fact-Checked**: Uses a secondary "Judge AI" to verify every response against grounded data, drastically reducing hallucinations.
- **Human-in-the-Loop**: Admins can review escalated tickets and "promote" user-suggested solutions to the global KB with one click.
- **Enterprise-Ready**: Secure authentication via Firebase and a responsive, modern Glassmorphism UI.

---

## ✨ Key Features
- **🤖 AI-Native Response Generation**: Powered by Google Gemini Flash with conversational memory.
- **🛡️ Cross-Verification (Judge AI)**: Secondary pass verification to ensure grounding in the Knowledge Base.
- **📈 Semantic Confidence Scoring**: Uses vector embeddings to calculate mathematical similarity between queries and documentation.
- **🔄 Learning Feedback Loop**: Captures "Not Helpful" responses and allows users to suggest corrections.
- **👨‍💻 Premium Admin Dashboard**: Real-time stats and management interface for ticket escalation and KB promotion.

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **AI Engine**: Google Generative AI (Gemini Flash, Text Embeddings)
- **Database**: Google Firestore (NoSQL)
- **Auth**: Firebase Authentication (Google & Email)
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), JavaScript (ES6+)

---

## 📂 Project Structure
```text
ResolveX/
├── app.py                  # Main Flask application & API routes
├── services/
│   ├── genai_service.py    # AI logic, Judge prompt, and Embeddings
│   └── firebase_service.py # Firestore and Auth integration
├── templates/              # HTML interfaces (Chat, Admin, Auth)
├── static/                 # CSS (styles.css) and JS (main.js)
├── docs/                   # Detailed documentation
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
└── firebase_credentials.json # (Required) Firebase Service Account key
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Firebase Project
- Google AI Studio API Key

### 2. Installation
```bash
git clone https://github.com/yourusername/ResolveX.git
cd ResolveX
pip install -r requirements.txt
```

### 3. Configuration
1. Copy `.env.example` to `.env` and fill in your keys.
2. Place your `firebase_credentials.json` in the root folder.

### 4. Run Locally
```bash
python app.py
```
Access the app at `http://127.0.0.1:5000`.

---

## 📚 Documentation
- [Setup Guide](docs/setup.md) - Comprehensive setup instructions.
- [API Reference](docs/api.md) - Documentation for all backend endpoints.
- [Architecture](docs/architecture.md) - Deep dive into the AI loop and similarity logic.
- [Usage Guide](docs/usage.md) - How to use the user and admin interfaces.

---

## 🖼️ Screenshots & Demos

### User Chat Interface
> ![User Chat Placeholder](https://via.placeholder.com/800x450?text=User+Chat+Interface+with+Glassmorphism+Design)
> *Caption: The main support interface featuring real-time AI responses and feedback forms.*

### Admin Dashboard
> ![Admin Dashboard Placeholder](https://via.placeholder.com/800x450?text=Admin+Dashboard+Preview)
> *Caption: Real-time analytics and ticket management for support administrators.*

### The Learning Loop in Action
> ![Feedback Loop Placeholder](https://via.placeholder.com/800x450?text=Learning+Feedback+Loop+GIF)
> *Caption: Demonstrating how user corrections are promoted to the Knowledge Base.*

---

## 🔮 Future Improvements
- [ ] Integration with Slack/Discord webhooks for admin notifications.
- [ ] Automated weekly PDF reports for support performance.
- [ ] Multi-language support using Gemini's translation capabilities.
- [ ] Vector database integration (e.g., Pinecone) for massive scale.

## 🤝 Contributors
- **Aditya Pandey** - Lead Developer & Architect

---
**ResolveX**: *Building support systems that actually get smarter.*
