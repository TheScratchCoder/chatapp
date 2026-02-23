# 💬 Real-Time Chat Application

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django)
![Django Channels](https://img.shields.io/badge/Django%20Channels-4.3-red?style=flat-square)
![Redis](https://img.shields.io/badge/Redis-7.0-red?style=flat-square&logo=redis)
![WebSocket](https://img.shields.io/badge/WebSocket-Enabled-brightgreen?style=flat-square)

A full-stack real-time chat application built with **Django**, **Django Channels**, and **WebSockets**. Users can register, create chat rooms, and exchange messages instantly without any page refresh.

---

## 🚀 Live Demo

> Coming soon — [TheScratchCoder.pythonanywhere.com](#)

---

## 🖥️ Screenshots

### 🔐 Login Page
Clean and minimal login interface

### 🏠 Chat Rooms
Browse and join available chat rooms

### 💬 Chat Room
Real-time messaging with Slack-inspired UI — messages appear instantly for all users

---

## ⚙️ Tech Stack

| Technology | Purpose |
|---|---|
| **Django 6.0** | Core web framework — routing, ORM, authentication |
| **Django Channels 4.3** | Upgrades Django from WSGI → ASGI for WebSocket support |
| **Daphne** | ASGI server — handles both HTTP and WebSocket connections |
| **Redis** | Channel layer — message bus that broadcasts to all room members |
| **SQLite** | Database — stores users, rooms, and message history |
| **Vanilla JS** | WebSocket client in the browser |

---

## 🏗️ Architecture

```
Browser (Vanilla JS WebSocket Client)
              ↕  WebSocket
   Django Channels (ASGI via Daphne)
              ↕  Channel Layer
            Redis  ←── broadcasts messages to all room members
              ↕
           SQLite  ←── saves message history
```

**Key concept:** Django by default is synchronous (WSGI). Django Channels upgrades it to **ASGI** which enables persistent **WebSocket** connections — making real-time messaging possible without polling.

---

## ✨ Features

- ✅ User Registration & Login (Django built-in auth)
- ✅ Create & Join Chat Rooms
- ✅ Real-Time messaging via WebSocket
- ✅ Message history loaded on room join
- ✅ Slack-inspired clean UI
- ✅ XSS protection on all messages
- ✅ Auto-scroll to latest message
- ✅ Instant message delivery (no page refresh)

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.12
- Redis server running on localhost:6379

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/TheScratchCoder/chatapp.git
cd chatapp
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start Redis**
```bash
# Ubuntu/WSL
sudo service redis-server start

# Mac
brew services start redis
```

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Start the server**
```bash
python manage.py runserver
```

**7. Open in browser**
```
http://localhost:8000
```

---

## 📁 Project Structure

```
chatapp/
├── chatproject/
│   ├── settings.py     # Django settings + Channel Layer config
│   ├── asgi.py         # ⭐ ASGI config — routes HTTP & WebSocket
│   └── urls.py         # Main URL patterns
│
├── chat/
│   ├── models.py       # Room & Message models
│   ├── consumers.py    # ⭐ WebSocket Consumer (real-time logic)
│   ├── routing.py      # WebSocket URL routing
│   ├── views.py        # HTTP views
│   ├── forms.py        # Register & Room forms
│   └── templates/
│       └── chat/
│           ├── base.html        # Base layout with sidebar
│           ├── login.html       # Login page
│           ├── register.html    # Register page
│           ├── room_list.html   # All rooms
│           ├── create_room.html # Create room
│           └── room_detail.html # ⭐ Chat UI + WebSocket JS
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔑 Key Files Explained

### `chatproject/asgi.py`
Routes incoming connections:
- HTTP → Django views (normal)
- WebSocket → Django Channels → ChatConsumer

### `chat/consumers.py`
The heart of real-time messaging:
- `connect()` — user joins room group in Redis channel layer
- `receive()` — message received → saved to DB → broadcast to group
- `disconnect()` — user removed from group

### `chat/templates/chat/room_detail.html`
WebSocket client:
- Opens WebSocket on page load
- Sends messages as JSON
- Receives broadcasts and renders them instantly

---

## 👨‍💻 Author

**Ankit Singh**
- GitHub: [@TheScratchCoder](https://github.com/TheScratchCoder)

