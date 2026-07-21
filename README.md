# Website Monitor with Telegram Notifications

A Python script that monitors websites for changes and sends Telegram notifications when updates are detected. Includes special keyword detection (e.g., "aamon" case-insensitive).

## Features

✅ Monitors website for content changes  
✅ Sends Telegram notifications on updates  
✅ Case-insensitive keyword detection  
✅ Custom alerts with extra notes  
✅ GitHub Actions integration  
✅ Persistent state tracking  
✅ Configurable check intervals  

## Setup

### 1. Prerequisites

- Python 3.7+
- Telegram Bot Token
- Telegram Chat ID

### 2. Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions
3. Save your bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyzABCDEfghi`)

### 3. Get Your Chat ID

1. Start a chat with your bot (`@Brut_mon_bot`)
2. Send any message to the bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your chat ID in the response (usually a negative number for groups or positive for users)

### 4. Configure

Edit `config.json`:

```json
{
  "telegram_token": "8888254841:AAGx3MGslz-ln2yGs9UjHvWSDbUckdEK9Is",
  "telegram_chat_id": "YOUR_CHAT_ID_HERE",
  "websites": [
    {
      "name": "Brutal Assault Accommodation",
      "url": "https://brutalassault.cz/en/accommodation?show=ao",
      "check_for_keyword": "aamon",
      "extra_note": "🎪 New element detected with 'aamon' keyword!"
    }
  ]
}
```

Replace `YOUR_CHAT_ID_HERE` with your actual Telegram chat ID.

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run Locally

```bash
python website_monitor.py
```

Press `Ctrl+C` to stop the monitor.

## GitHub Actions Setup

The workflow runs automatically every 5 minutes.

### Add Secrets

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Create `TELEGRAM_BOT_TOKEN` with: `8888254841:AAGx3MGslz-ln2yGs9UjHvWSDbUckdEK9Is`
3. Create `TELEGRAM_CHAT_ID` with your chat ID from `@Brut_mon_bot`

The workflow will:
- Install dependencies
- Create config with secrets
- Run the monitor for 60 seconds
- Check 12 times per hour

## How It Works

1. **First Run**: Fetches initial content and stores hash
2. **Subsequent Runs**: Compares content hash with stored version
3. **Change Detected**: 
   - Sends notification with change details
   - Updates stored hash
   - Checks for keywords in new content
4. **Keyword Match**: Sends additional alert with extra note

## Notifications

### Standard Change Alert
```
🚨 Website Changed!

Site: Brutal Assault Accommodation
URL: https://brutalassault.cz/en/accommodation?show=ao
Time: 2024-01-15T10:30:45.123456

Content has been updated.
```

### Keyword Alert
```
⚠️ Keyword Alert!
Found 'aamon' 2 time(s) in the updated content.

🎪 New element detected with 'aamon' keyword!
```

## File Structure

```
.
├── website_monitor.py      # Main monitoring script
├── config.json             # Configuration file (update with your chat ID)
├── requirements.txt        # Python dependencies
├── monitor_state.json      # Generated automatically (state tracking)
├── .github/
│   └── workflows/
│       └── main.yml        # GitHub Actions workflow
└── README.md              # This file
```

## Troubleshooting

### No notifications received
- Check Telegram bot token is correct: `8888254841:AAGx3MGslz-ln2yGs9UjHvWSDbUckdEK9Is`
- Verify chat ID is correct (send a message to `@Brut_mon_bot` and check logs)
- Start a chat with the bot and send `/start`
- Verify bot has message permissions

### Changes not detected
- Website might use JavaScript to load content (would need Selenium/Playwright)
- Website might be blocking requests (User-Agent header included)
- Check logs for HTTP errors

### Script crashes
- Verify `requests` package is installed: `pip install -r requirements.txt`
- Check `config.json` is valid JSON
- Ensure URL is accessible

## Check Interval

- **Local**: Default 300 seconds (5 minutes)
- **GitHub Actions**: Runs every 5 minutes for 60 seconds per run
- **Modify**: Change `check_interval` parameter in `monitor.monitor()` call

## Monitored Website

**Brutal Assault Accommodation**
- URL: https://brutalassault.cz/en/accommodation?show=ao
- Keyword: "aamon" (case-insensitive)
- Alert: 🎪 New element detected with 'aamon' keyword!

## Bot Details

- **Bot Name**: @Brut_mon_bot
- **Bot Token**: 8888254841:AAGx3MGslz-ln2yGs9UjHvWSDbUckdEK9Is

## License

Free to use and modify.
