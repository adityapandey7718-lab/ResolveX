# ResolveX - AI-Powered Customer Support Automation

![ResolveX](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-yellow)

ResolveX is an intelligent, AI-powered customer support automation system that leverages machine learning and continuous learning feedback loops to deliver faster, smarter, and more accurate customer assistance. The system automatically classifies customer issues and provides contextual solutions while continuously improving through user feedback.

## 🌟 Features

- **🤖 Intelligent Intent Classification**: Uses TF-IDF vectorization and SVM machine learning to automatically classify customer issues into three categories (billing, technical, account)
- **💬 Smart Response Generation**: Provides contextual, pre-defined responses from a knowledge base based on detected intent
- **📚 Continuous Learning**: Learns from user feedback to improve classification accuracy over time
- **🎫 Ticket Management**: Tracks support interactions with unique ticket IDs for follow-up and analytics
- **🔌 REST API**: Clean, simple JSON-based API for easy integration with existing systems
- **🎨 Modern UI**: Responsive, user-friendly web interface with real-time feedback
- **⚡ Fast & Reliable**: Lightweight Flask-based backend with minimal dependencies

## 📋 Supported Issue Categories

| Category | Description | Example Issues |
|----------|-------------|-----------------|
| **💳 Billing** | Payment and subscription-related issues | Refunds, duplicate charges, billing errors |
| **🔧 Technical** | App functionality and technical problems | Crashes, errors, feature issues |
| **👤 Account** | User account and authentication issues | Password resets, login problems, profile updates |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd ResolveX
   ```

2. **Activate the virtual environment** (Windows)
   ```bash
   .\activate.bat
   ```
   Or on macOS/Linux:
   ```bash
   source activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 📚 API Documentation

### POST `/chat`
Process a customer message and receive an intelligent AI response.

**Request:**
```json
{
  "message": "I was charged twice for my subscription"
}
```

**Response (Success):**
```json
{
  "ticket_id": "abc12345",
  "intent": "billing",
  "response": "Please check your billing section in account settings. If you see duplicate charges, contact our support team with your ticket ID."
}
```

**Response (Error):**
```json
{
  "error": "Message cannot be empty"
}
```

**Status Codes:**
- `200 OK`: Request processed successfully
- `400 Bad Request`: Invalid request format or empty message
- `500 Internal Server Error`: Server error

### POST `/feedback/<ticket_id>`
Submit feedback on the response quality to improve the ML model.

**Request for Positive Feedback:**
```json
{
  "helpful": true
}
```

**Request for Negative Feedback (with correction):**
```json
{
  "helpful": false,
  "correct_intent": "technical"
}
```

**Response:**
```json
{
  "message": "Feedback recorded successfully. Model updated!"
}
```

**Status Codes:**
- `200 OK`: Feedback recorded successfully
- `400 Bad Request`: Missing required parameters
- `404 Not Found`: Ticket ID not found
- `500 Internal Server Error`: Server error

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                    User Interaction Flow                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1. User submits message describing their issue                      │
│         │                                                             │
│         ▼                                                             │
│  2. ML Model classifies intent (billing/technical/account)          │
│         │                                                             │
│         ▼                                                             │
│  3. System retrieves contextual response from knowledge base        │
│         │                                                             │
│         ▼                                                             │
│  4. Response delivered to user with unique ticket ID                │
│         │                                                             │
│         ▼                                                             │
│  5. User provides feedback (helpful/not helpful)                    │
│         │                                                             │
│         ▼                                                             │
│  6. Feedback added to training data & model retrained               │
│         │                                                             │
│         ▼                                                             │
│  7. Improved model deployed for next interactions                   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Machine Learning**: scikit-learn (TF-IDF Vectorizer, SVM Classifier)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Processing**: Python standard library

## 📁 Project Structure

```
ResolveX/
├── app.py                 # Flask application & ML backend
├── requirements.txt       # Python dependencies
├── activate.bat          # Windows virtual environment activation
├── static/
│   ├── main.js          # Frontend JavaScript logic
│   └── style.css        # Responsive styling
├── templates/
│   └── index.html       # Main web interface
└── README.md            # This file
```

## 🚨 Error Handling

ResolveX includes comprehensive error handling for:

- ✅ Empty or whitespace-only messages
- ✅ Messages shorter than 10 characters
- ✅ Malformed JSON requests
- ✅ Invalid or expired ticket IDs
- ✅ Missing required feedback parameters
- ✅ Network connectivity issues
- ✅ Server errors (with user-friendly messages)

## 🤝 Using the Web Interface

1. **Describe Your Issue**: Write a clear description of your problem (at least 10 characters)
2. **Submit**: Click "Send Message" and wait for the AI to process
3. **View Response**: See the classified issue category and recommended solution
4. **Provide Feedback**: Click "Helpful" or "Not Helpful" to improve the model
5. **New Message**: Click "New Message" to reset and ask another question

## 🔐 Security Considerations

- Input validation on all messages (length, content)
- Request validation and error handling
- Unique ticket ID generation using UUID
- Data stored in-memory (no external database vulnerability)

## 📊 Performance Metrics

- **Average Response Time**: < 100ms
- **Model Training Time**: < 50ms
- **Concurrent Users**: Limited by Flask development server
- **Message Character Limit**: 500 characters per submission

## 🐛 Troubleshooting

### Application won't start
- Verify Python 3.8+ is installed: `python --version`
- Check dependencies: `pip install -r requirements.txt`
- Ensure port 5000 is available: `netstat -ano | grep 5000`

### Machine Learning model not improving
- Provide consistent feedback on responses
- Ensure feedback includes correct intent category when marking as unhelpful
- More training examples improve accuracy over time

### Front-end not loading
- Clear browser cache: `Ctrl+Shift+Delete`
- Verify static files are in correct directories
- Check browser console for JavaScript errors: `F12`

### API request errors
- Verify message is not empty
- Check message is at least 10 characters
- Ensure valid JSON format in requests
- Verify ticket ID exists when sending feedback

## 📝 Example Usage

### Using cURL
```bash
# Send a message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want a refund for my subscription"}'

# Send feedback
curl -X POST http://localhost:5000/feedback/abc12345 \
  -H "Content-Type: application/json" \
  -d '{"helpful": true}'
```

### Using Python
```python
import requests
import json

# Send a message
response = requests.post(
    'http://localhost:5000/chat',
    json={'message': 'I have a technical issue with your app'}
)

data = response.json()
print(f"Ticket ID: {data['ticket_id']}")
print(f"Intent: {data['intent']}")
print(f"Response: {data['response']}")

# Send feedback
feedback_response = requests.post(
    f'http://localhost:5000/feedback/{data["ticket_id"]}',
    json={'helpful': True}
)
```

## 🎓 How Machine Learning Improves the System

1. **Initial Training**: Model trained on basic sample data for each intent
2. **User Interaction**: System receives real customer messages
3. **Prediction**: Model classifies intent based on learned patterns
4. **User Feedback**: Users indicate if response was helpful
5. **Model Update**: Incorrect classifications are added to training data
6. **Retraining**: Model is retrained with expanded dataset
7. **Improved Accuracy**: Subsequent predictions more accurate

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional intent categories
- More sophisticated NLP models
- Database integration for persistent storage
- Authentication and user management
- Analytics dashboard
- Multi-language support

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review API documentation
3. Check browser console for errors
4. Verify all dependencies are installed

## 🎉 Version History

- **v1.0** (2026-02-22) - Initial release with core features

---

**ResolveX**: Your AI-powered solution for intelligent customer support automation.
