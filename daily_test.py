#!/usr/bin/env python3
"""
Daily Test Message Sender
Sends a daily test message via Telegram to verify the bot is working
"""

import requests
import json
from datetime import datetime
from pathlib import Path


def send_daily_test_message():
    """Send daily test message to verify monitor is active"""
    
    # Load config
    config_file = Path('config.json')
    if not config_file.exists():
        print("Error: config.json not found")
        return False
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    telegram_token = config.get('telegram_token')
    telegram_chat_id = config.get('telegram_chat_id')
    
    if not telegram_token or not telegram_chat_id:
        print("Error: Telegram credentials not configured")
        return False
    
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    timestamp = datetime.now().isoformat()
    
    message = (
        f"✅ <b>Daily Monitor Check</b>\n\n"
        f"<b>Status:</b> Active and running\n"
        f"<b>Time:</b> {timestamp}\n"
        f"<b>Website:</b> Brutal Assault Accommodation\n"
        f"<b>URL:</b> https://brutalassault.cz/en/accommodation?show=ao\n"
        f"<b>Keyword:</b> aamon (case-insensitive)\n\n"
        f"✓ Monitor is operational\n"
        f"✓ Checking for website changes\n"
        f"✓ Ready to alert on updates"
    )
    
    payload = {
        'chat_id': telegram_chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Daily test message sent successfully at {timestamp}")
        return True
    except requests.RequestException as e:
        print(f"❌ Failed to send test message: {e}")
        return False


if __name__ == "__main__":
    send_daily_test_message()
