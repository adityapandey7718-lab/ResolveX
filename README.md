# ResolveX

ResolveX is an AI-powered customer support automation system that uses intelligent response generation and learning feedback loops to continuously improve support quality. It adapts from user interactions to deliver faster, smarter, and more accurate customer assistance.

## Features

- **Intent Classification**: Uses TF-IDF vectorization and SVM machine learning to automatically classify customer issues into categories (billing, technical, account)
- **Intelligent Response Generation**: Provides contextual responses from a knowledge base based on detected intent
- **Continuous Learning**: Learns from user feedback to improve classification accuracy over time
- **Ticket Management**: Tracks support tickets with unique IDs for follow-up and feedback
- **REST API**: Simple JSON-based API for easy integration

## Supported Intent Categories

- **billing**: Issues related to refunds, charges, and billing problems
- **technical**: Technical issues, errors, and app functionality problems
- **account**: Account-related issues like password resets and login problems

## API Endpoints

### POST `/chat`
Process a customer message and get an intelligent response.

**Request:**
```json
{
  "message": "I was charged twice for my subscription"
}
```

**Response:**
```json
{
  "ticket_id": "abc12345",
  "intent": "billing",
  "response": "Please check your billing section in account settings."
}
```

### POST `/feedback/<ticket_id>`
Submit feedback on the response quality to improve the model.

**For Positive Feedback:**
```json
{
  "helpful": true
}
```

**For Negative Feedback (with correction):**
```json
{
  "helpful": false,
  "correct_intent": "technical"
}
```

## How It Works

1. **Initial Classification**: When a user submits a message, the trained ML model classifies it into one of the supported intent categories
2. **Response Delivery**: Based on the detected intent, a pre-defined response is returned to address the customer's issue
3. **Feedback Loop**: Users can rate whether the response was helpful
4. **Model Improvement**: When negative feedback is provided with the correct intent, the system adds this data to its training set and retrains the model
5. **Continuous Adaptation**: Over time, the model becomes more accurate at classifying customer issues based on real-world interactions

## Error Handling

The system includes comprehensive error handling for:
- Empty or invalid messages
- Malformed requests
- Invalid ticket IDs
- Missing required feedback parameters

## Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`
