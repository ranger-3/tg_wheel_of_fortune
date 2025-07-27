# ✈️ Telegram Bot with WebApp: Wheel of Fortune

This project combines a Telegram bot and a FastAPI WebApp. Users who are subscribed to a specific Telegram channel can spin a wheel once per week to receive unique promo codes. The backend validates users via Telegram WebApp `initData`.

---

## 📦 Requirements

- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- Public HTTPS endpoint (for WebApp to work — use [ngrok](https://ngrok.com/)/[Render](https://render.com/)/etc.)

---

## 🛠 Setup

1. **Create `.env` file**

```env
BOT_TOKEN=your_bot_token
CHANNEL_USERNAME=@your_channel_username
WEBAPP_URL=https://your-webapp-url.example.com
```

Explanation:
- `BOT_TOKEN`: Token from [@BotFather](https://telegram.me/BotFather)
- `CHANNEL_USERNAME`: Your Telegram channel (including `@`)
- `WEBAPP_URL`: Public HTTPS URL of the backend (required for Telegram WebApp)

2. **Start with Docker Compose**

```bash
docker compose up --build
```

Both the bot and backend will be built and launched in their containers.
