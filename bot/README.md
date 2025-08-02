## ⚙️ Local Development Setup (without Docker)

This guide explains how to run the Telegram bot locally using [`uv`](https://docs.astral.sh/uv/getting-started/installation/) — a fast Python package manager.


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
WEBAPP_URL=                # HTTPS URL of your Telegram WebApp
```

**Notes:**
- `BOT_TOKEN` — get it from [@BotFather](https://t.me/BotFather)
- `CHANNEL_USERNAME`: Username of your Telegram channel — make sure it starts with @, like @mychannel
- `WEBAPP_URL` — public HTTPS endpoint for your WebApp (e.g. from [ngrok](https://ngrok.com) or [Render](https://render.com))

---

### ▶️ 3. Run the bot

Start the bot in development mode using:

```bash
uv run app.py
```

If everything is configured correctly, you should see in logs:

```
Bot is up and running...
```

---

### 🧪 4. Test the flow

- Open Telegram and send `/start` to your bot
- If subscribed to the channel — you’ll see a button to open the WebApp
- Otherwise — the bot will ask you to subscribe first

---

### ⚠️ Troubleshooting

- `.env` not found or invalid? Double-check the file path and variable values
- `WEBAPP_URL` must start with `https://`
- Issues with Telegram API? Make sure the bot token is correct and your internet connection is stable
