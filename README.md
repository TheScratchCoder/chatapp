# 💬 Real-Time Chat Application

A real-time chat application built with **Django**, **Django Channels**, **WebSockets**, and **Redis**.

---

## 🚀 Tech Stack

| Technology       | Purpose                                      |
|-----------------|----------------------------------------------|
| Django           | Core web framework (routing, ORM, auth)      |
| Django Channels  | Upgrades Django to handle WebSockets (ASGI)  |
| Daphne           | ASGI server (replaces default Django server) |
| Redis            | Channel layer — message bus between users    |
| SQLite           | Database (stores users, rooms, messages)     |
| Vanilla JS       | WebSocket client in the browser              |

---

## 🏗️ How It Works

```
Browser (Vanilla JS WebSocket)
         ↕  WebSocket Connection
Django Channels (ASGI via Daphne)
         ↕  Channel Layer
       Redis  ← broadcasts to all room members
         ↕
       SQLite ← saves message history
```

**Key concept:** Django normally uses WSGI (synchronous, HTTP only).
Django Channels upgrades it to **ASGI** which supports **WebSockets** —
persistent two-way connections that enable real-time messaging without polling.

---

## ✅ Features

- User Registration & Login (Django built-in auth)
- Create & Join Chat Rooms
- Real-Time messaging via WebSocket
- Message history (last 20 messages loaded on join)
- Clean WhatsApp-inspired UI
- XSS protection on all messages

---

## 🛠️ Setup & Run

### Step 1 — Clone & Install

```bash
git clone <your-repo-url>
cd chatapp

pip install -r requirements.txt
```

### Step 2 — Start Redis

Make sure Redis is running on localhost:6379

```bash
# On Mac (Homebrew)
brew install redis
brew services start redis

# On Ubuntu/Linux
sudo apt install redis-server
sudo systemctl start redis

# On Windows — use WSL or download Redis for Windows
```

### Step 3 — Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4 — Create Superuser (optional, for admin panel)

```bash
python manage.py createsuperuser
```

### Step 5 — Run the Server

```bash
python manage.py runserver
```

> **Note:** Daphne (ASGI server) is automatically used because we added
> `daphne` to INSTALLED_APPS. This enables WebSocket support.

### Step 6 — Open in Browser

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
│   ├── views.py        # Regular HTTP views
│   ├── forms.py        # Register & Room forms
│   ├── urls.py         # HTTP URL patterns
│   └── templates/
│       └── chat/
│           ├── base.html        # Base layout
│           ├── login.html       # Login page
│           ├── register.html    # Register page
│           ├── room_list.html   # Home — list of rooms
│           ├── create_room.html # Create room form
│           └── room_detail.html # ⭐ Chat UI + WebSocket JS
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔑 Key Files to Understand

### `chatproject/asgi.py`
Routes incoming connections:
- HTTP requests → Django views (normal)
- WebSocket requests → Django Channels → ChatConsumer

### `chat/consumers.py`
The heart of real-time messaging:
- `connect()` — user joins room group in Redis
- `receive()` — message received → saved to DB → broadcast to group
- `disconnect()` — user removed from group

### `chat/templates/chat/room_detail.html`
WebSocket client in JavaScript:
- Opens WebSocket connection on page load
- Sends messages to server as JSON
- Receives broadcast messages and renders them in the UI

---

## 💡 Interview Explanation

> "I built a real-time chat app using Django and Django Channels.
> By default Django is synchronous (WSGI), but Django Channels upgrades it
> to ASGI which enables WebSocket support — persistent two-way connections
> between browser and server. Redis acts as the channel layer, a message bus
> that broadcasts messages to all users connected to the same room.
> Messages are also saved to SQLite so history loads when you join a room."

---

## 📸 Screenshots

### Home — Room List
- Clean grid of available chat rooms
- Create new room button

### Chat Room
- Real-time messages with WhatsApp-inspired bubbles
- Your messages appear on the right (green)
- Others' messages appear on the left (white)
- Message history loaded from database on join

---

## 🙏 Built with ❤️ using Django + Django Channels
