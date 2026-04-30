# Setup Guide

This guide will help you set up ResolveX for local development.

## Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: (Optional) if you plan to use any modern build tools, though current project uses Vanilla JS.
- **Firebase Account**: Access to Firebase Console.
- **Google AI Studio Account**: For Gemini API access.

---

## 1. Local Environment Setup

### Clone the Repository
```bash
git clone https://github.com/yourusername/ResolveX.git
cd ResolveX
```

### Create a Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 2. Firebase Configuration

### Create a Project
1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Click **Add project** and follow the setup steps.

### Setup Firestore Database
1. In the sidebar, click **Build > Firestore Database**.
2. Click **Create database** and choose a location.
3. Start in **Test mode** for initial development (or production with proper rules).

### Setup Firebase Authentication
1. Click **Build > Authentication**.
2. Click **Get Started**.
3. Enable **Email/Password** and **Google** sign-in methods.

### Get Admin SDK Credentials
1. Click the **Gear icon (Project settings)** > **Service accounts**.
2. Click **Generate new private key**.
3. Download the JSON file and save it as `firebase_credentials.json` in the root of the ResolveX project.

### Get Web Client Config
1. Go to **Project settings > General**.
2. Scroll to **Your apps** and click the `</>` (Web) icon.
3. Register the app (e.g., "ResolveX-Web").
4. Copy the `firebaseConfig` object values. You will need these for your `.env` file.

---

## 3. Google AI Studio Setup

1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API key**.
3. Generate a new API key and copy it.

---

## 4. Environment Variables

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in the values:
   - `GOOGLE_API_KEY`: Your Gemini API key.
   - `FIREBASE_PROJECT_ID`: Your Firebase Project ID.
   - Fill in the `FIREBASE_API_KEY`, `FIREBASE_AUTH_DOMAIN`, etc., from the Web Client config.

---

## 5. Running the Application

1. Ensure your virtual environment is active.
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Troubleshooting

### Firebase Token Errors
If you see "Token used too early", it might be due to system clock drift. The application includes a retry mechanism for this, but ensuring your system clock is synchronized helps.

### Firestore Permission Denied
Ensure you have created the `tickets` and `knowledge_base` collections in Firestore, or that your security rules allow the Admin SDK to create them automatically.
