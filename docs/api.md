# API Documentation

This document describes the backend API endpoints available in ResolveX.

## Base URL
The default local development URL is `http://127.0.0.1:5000`.

---

## Authentication Endpoints

### Verify Auth Token
**Method**: `POST`  
**Route**: `/api/auth/verify`  
**Purpose**: Verifies a Firebase ID token and establishes a Flask session.

**Request Body**:
```json
{
  "idToken": "FIREBASE_ID_TOKEN_STRING"
}
```

**Response (Success - 200)**:
```json
{
  "success": true,
  "message": "Authenticated"
}
```

**Response (Error - 401)**:
```json
{
  "error": "Invalid token"
}
```

---

## Chat & Tickets Endpoints

### AI Chat
**Method**: `POST`  
**Route**: `/chat`  
**Purpose**: Sends a user message to the AI and receives a support response. Automatically creates/updates a ticket in Firestore.  
**Requirement**: Authentication required.

**Request Body**:
```json
{
  "message": "My payment failed but I was charged.",
  "ticket_id": "optional_ticket_id"
}
```

**Response (200)**:
```json
{
  "ticket_id": "ab12cd34",
  "intent": "billing",
  "response": "I'm sorry to hear about the payment issue. Please check your bank...",
  "confidence": 85,
  "status": "Resolved"
}
```

---

### Submit Feedback
**Method**: `POST`  
**Route**: `/feedback/<ticket_id>`  
**Purpose**: Allows users to rate an AI response and provide corrections if the response was unhelpful.  
**Requirement**: Authentication required.

**Request Body**:
```json
{
  "helpful": false,
  "correct_answer": "You should contact the billing department at billing@example.com",
  "correct_category": "billing"
}
```

**Response (200)**:
```json
{
  "message": "Feedback recorded"
}
```

---

### Get Ticket Details
**Method**: `GET`  
**Route**: `/api/ticket/<ticket_id>`  
**Purpose**: Retrieves details for a specific ticket.  
**Requirement**: Authentication required.

**Response (200)**:
```json
{
  "id": "ab12cd34",
  "user_id": "user123",
  "message": "User query",
  "response": "AI response",
  "intent": "technical",
  "confidence": 90,
  "status": "Resolved",
  "feedback": "positive"
}
```

---

## Admin Endpoints

### Update Ticket (Admin)
**Method**: `POST`  
**Route**: `/api/admin/ticket/<ticket_id>`  
**Purpose**: Allows admins to manually update a ticket's status or response.  
**Requirement**: Authentication required.

**Request Body**:
```json
{
  "status": "Resolved",
  "response": "Updated human-verified response"
}
```

**Response (200)**:
```json
{
  "success": true
}
```

---

### Update Knowledge Base (Admin)
**Method**: `POST`  
**Route**: `/api/admin/kb`  
**Purpose**: Adds or updates an entry in the Knowledge Base. This is used when an admin "promotes" a user-suggested correction to the KB.  
**Requirement**: Authentication required.

**Request Body**:
```json
{
  "intent": "billing_refund_policy",
  "response": "Refunds are processed within 5-7 business days."
}
```

**Response (200)**:
```json
{
  "success": true
}
```

---

## Error Handling
All API endpoints return JSON. Common error responses include:
- `400 Bad Request`: Missing required fields or invalid format.
- `401 Unauthorized`: Missing or invalid session/token.
- `404 Not Found`: Ticket or resource does not exist.
- `500 Internal Server Error`: Server-side exception.
