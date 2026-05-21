# Real-Time Chat Application — Backend

A scalable real-time chat backend built with Django, Django REST Framework, and Django Channels.

This service powers authentication, conversations, message persistence, offline synchronization, and real-time communication using WebSockets.

---

## Architecture Overview

The backend is responsible for:

* User authentication and authorization
* REST APIs for messaging and conversations
* Real-time communication via WebSockets
* Offline message persistence
* User room management
* Event-driven message broadcasting

Frontend Repository:

* Built with React
* Connects to this backend via REST APIs and WebSocket connections

---

## Tech Stack

* Python
* Django
* Django REST Framework
* Django Channels
* Redis (Channel Layer)
* PostgreSQL
* WebSockets

---

## System Design Principles

### 1. Separation of Concerns

The system separates:

* REST APIs → Persistence & authentication
* WebSockets → Real-time communication
* Signals → Event broadcasting
* Database → Long-term storage

This makes the architecture modular and easier to scale.

---

### 2. Real-Time Messaging Architecture

When a message is sent:

1. The frontend calls the Messages API
2. The message is persisted in PostgreSQL
3. A Django signal is triggered
4. The signal publishes the event through the channel layer
5. Django Channels broadcasts the message to the receiver’s room
6. If the receiver is offline, the message remains stored for retrieval later

---

### 3. User Room Management

Each authenticated user is assigned to a dedicated WebSocket room.

This allows:

* Direct messaging
* Efficient event broadcasting
* Presence tracking
* Scalable communication patterns

---

### 4. Offline Message Synchronization

Messages are stored before broadcasting.

This guarantees:

* Message durability
* Offline access
* Synchronization across sessions

---

## Backend Structure

```bash
backend/
│
├── authentication/
├── chat/
├── conversations/
├── websocket/
├── signals/
├── consumers/
├── serializers/
├── views/
├── routing.py
└── settings.py
```

---

## API Responsibilities

### Authentication APIs

* Login
* Registration
* JWT authentication

### Messaging APIs

* Save messages
* Load conversation history
* Retrieve offline messages

### Conversation APIs

* User connections
* Conversation management

---

## WebSocket Responsibilities

The WebSocket layer handles:

* Real-time message delivery
* Presence updates
* Room subscriptions
* Connection lifecycle management

---

## Redis Channel Layer

Redis is used as the channel layer for:

* Pub/Sub communication
* Cross-consumer event broadcasting
* Scalable message fan-out

---

## Running the Project

### Clone Repository

```bash
git clone <backend-repo-url>
cd backend
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=chat_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

### Run Migrations

```bash
python manage.py migrate
```

---

### Start Server

```bash
python manage.py runserver
```

---

### Start Redis

```bash
redis-server
```

---

## Relationship With Frontend

The React frontend communicates with this backend using:

### REST APIs

Used for:

* Authentication
* Loading messages
* Fetching conversations
* Persisting chat history

### WebSockets

Used for:

* Real-time messaging
* Presence updates
* Instant event broadcasting

---

## Research & Scalability Notes

During development, research was conducted on how large-scale messaging platforms manage persistent socket connections.

Particular attention was given to WhatsApp’s Erlang-based architecture for:

* High concurrency
* Low memory consumption
* Efficient connection handling

These concepts influenced the event-driven design approach used in this project.

---

## Future Improvements

* Typing indicators
* Read receipts
* Message queues
* Horizontal scaling
* Kubernetes deployment
* Distributed WebSocket workers
* Media uploads

---

## License

MIT License
