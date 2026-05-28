# Django REST Framework Practices & Projects Backend

A collection of backend practices and mini-projects built with **Django**, **Django REST Framework**, and supporting technologies.

This repository serves as a centralized backend workspace where each practice/project is implemented with **its own endpoint and isolated logic**, making experimentation, learning, and scalability easier.

The goal of this repository is to explore:

- REST API development
- Authentication systems
- Real-time communication
- Database architecture
- Scalable backend patterns
- System design concepts
- Backend performance strategies

---

# Project Philosophy

Each practice/project in this repository follows a **modular architecture**:

- Independent endpoints
- Separate business logic
- Isolated serializers, views, and services

---

# Frontend Practices

### 1. TodoList App — Frontend

A simple TodoList application built to demonstrate fundamental CRUD operations.

Features:

- Create todos
- Read todos
- Update todos
- Delete todos
- Searching
- Ordering
- Filtering

---

# Backend Practices & Projects

## 1. Real-Time Chat Application

A scalable real-time chat backend built using:

- Python
- Django
- Django REST Framework
- Django Channels
- Redis
- PostgreSQL
- WebSockets

### Overview

This module powers:

- Authentication & authorization
- Conversations
- Real-time messaging
- Offline synchronization
- Presence management
- Event-driven broadcasting

### System Design

The chat architecture separates responsibilities into independent layers:

#### REST APIs

Responsible for:

- Authentication
- Message persistence
- Conversation retrieval
- Offline synchronization

#### WebSockets

Responsible for:

- Real-time message delivery
- Presence tracking
- Room subscriptions
- Connection lifecycle management

#### Redis Channel Layer

Used for:

- Pub/Sub communication
- Cross-consumer broadcasting
- Message fan-out

---

### Messaging Flow

When a message is sent:

1. Frontend sends a request to the Messages API
2. Message is persisted in PostgreSQL
3. Django signals are triggered
4. Event is published through Redis channel layer
5. Django Channels broadcasts to recipient room
6. Offline users retrieve stored messages later

---

### User Room Management

Each authenticated user is assigned to a dedicated WebSocket room.

Benefits:

- Direct messaging
- Efficient broadcasting
- Presence management
- Scalable communication

---

### Offline Synchronization

Messages are stored before broadcast.

This guarantees:

- Message durability
- Offline access
- Session synchronization

---

# Backend Structure

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
├── settings.py
└── ...
```

---

# API Responsibilities

## Authentication APIs

- Login
- Registration
- JWT Authentication

## Messaging APIs

- Save messages
- Load conversation history
- Retrieve offline messages

## Conversation APIs

- User connections
- Conversation management

---

# Research & Architecture Notes

During development, research was conducted into large-scale messaging systems and persistent socket architectures.

Particular inspiration came from WhatsApp’s Erlang-based architecture regarding:

- High concurrency
- Low memory usage
- Efficient connection handling
- Event-driven communication

These ideas influenced the system design decisions used in the chat module.

---

# Running the Project

## Clone Repository

```bash
git clone https://github.com/mike0001-prog/pratices-backend.git
cd pratices-backend
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

## Run Migrations

```bash
python manage.py migrate
```

---

## Start Django Server

```bash
python manage.py runserver
```

---

# Relationship With Frontend

Frontend applications communicate with this backend using:

## REST APIs

Used for:

- Authentication
- Data persistence
- Fetching resources
- Business logic execution

## WebSockets

Used for:

- Real-time communication
- Presence updates
- Event broadcasting

---

---

---

# License

MIT License
