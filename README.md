# ResolveX - Intelligent AI Support with Learning Feedback Loops

![ResolveX](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![Flask](https://img.shields.io/badge/Flask-3.0-yellow)
![AI](https://img.shields.io/badge/Gemini-Flash--Latest-orange)

ResolveX is a self-improving AI customer support automation system. Unlike traditional chatbots, ResolveX features a **Learning Feedback Loop** where it captures unresolved queries and agent corrections to continuously improve its Knowledge Base.

## 🌟 Key Features

- **🤖 AI-Native Response Generation**: Powered by Google Gemini Flash with dynamic RAG (Retrieval-Augmented Generation).
- **🛡️ Cross-Verification (Judge AI)**: Every response is verified by a secondary "Judge" prompt to prevent hallucinations and ensure grounding in the Knowledge Base.
- **📈 Semantic Confidence Scoring**: Uses `text-embedding-004` to calculate the mathematical similarity between user queries and known documentation.
- **🔄 Learning Feedback Loop**: captures "Not Helpful" responses and allows users to suggest corrections.
- **👨‍💻 Human-in-the-Loop Dashboard**: A premium admin interface to review escalated tickets and promote corrections to the Knowledge Base with one click.
- **🔐 Enterprise Security**: Firebase Authentication (Google & Email) and secure environment management.

## 🔄 The Learning Loop
1. **User Query**: User asks a question.
2. **AI Analysis**: System calculates semantic similarity and verifies grounding.
3. **Escalation**: If confidence is low (<60%), the ticket is marked as "Escalated."
4. **Feedback**: User can mark a response as "Not Helpful" and provide the correct solution.
5. **Human Oversight**: Admin reviews the correction in the Dashboard.
6. **Knowledge Injection**: Admin clicks "To KB," and the AI instantly learns the new solution for future queries.

## 🚀 Tech Stack
- **Backend**: Flask (Python 3.13)
- **AI/ML**: Google Generative AI (Gemini Flash, Text Embeddings)
- **Database**: Google Firestore (NoSQL)
- **Auth**: Firebase Authentication
- **Frontend**: Vanilla JS, CSS3 (Glassmorphism design)

## 📁 Project Structure
- `app.py`: Main Flask application and API routes.
- `services/genai_service.py`: AI logic, Judge prompt, and Embedding similarity.
- `services/firebase_service.py`: Firestore and Auth integration.
- `templates/admin.html`: Interactive Human-in-the-Loop dashboard.
- `templates/index.html`: User chat interface with feedback form.
- `static/main.js`: Frontend logic and interactive UI.

## 🛠️ Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set up your `.env` file with `GOOGLE_API_KEY` and Firebase config.
4. Run the app: `python app.py`.

---
**ResolveX**: *Building support systems that actually get smarter.*
