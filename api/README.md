## ⚙️ Local Backend API Setup (without Docker)

This guide explains how to run the backend API locally using [`uv`](https://docs.astral.sh/uv/getting-started/installation/) — a fast Python package manager.


---

### 📦 1. Install dependencies

Run this from the root of your project (where `pyproject.toml` is located):

```bash
uv sync
```

This will install all required packages.

---

### 🔐 2. Create `.env` file

In the same folder as `app.py`, create a `.env` file with the following variables:

```env
BOT_TOKEN=                 # Telegram bot token from @BotFather (keep secret)
CHANNEL_USERNAME=          # Channel username (must start with @)

STORE_API_KEY=             # Store API access key (keep secret)
STORE_API_URL=             # Endpoint to create promo codes in store
```

**Notes:**
- `BOT_TOKEN` — get it from [@BotFather](https://t.me/BotFather)
- `CHANNEL_USERNAME`: Username of your Telegram channel — make sure it starts with @, like @mychannel

---

### ▶️ 3. Run the API server

Start the FastAPI backend using:


```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

This setup uses multiple processes.

---

### ✅ API should now be available at:

```
http://localhost:8000
```
