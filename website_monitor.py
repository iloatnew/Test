#!/usr/bin/env python3
"""
Website Monitor with Telegram Notifications
Monitors a website for changes and sends alerts via Telegram
Special detection for keywords like "aamon" (case-insensitive)
"""

import requests
import hashlib
import time
import json
from datetime import datetime
from pathlib import Path
import logging
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebsiteMonitor:
    def __init__(self, config_file='config.json'):
        """Initialize the website monitor with configuration"""
        self.config = self._load_config(config_file)
        self.state_file = Path('monitor_state.json')
        self.state = self._load_state()
        
    def _load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {config_file} not found")
            raise
    
    def _load_state(self):
        """Load previous state of monitored websites"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_state(self):
        """Save current state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _get_content_hash(self, content):
        """Generate SHA256 hash of content"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def fetch_website(self, url, timeout=10):
        """Fetch website content"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def send_telegram_notification(self, message):
        """Send notification via Telegram"""
        telegram_token = self.config.get('telegram_token')
        telegram_chat_id = self.config.get('telegram_chat_id')
        
        if not telegram_token or not telegram_chat_id:
            logger.warning("Telegram credentials not configured")
            return False
        
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            'chat_id': telegram_chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Telegram notification sent successfully")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False
    
    def check_for_keyword(self, content, keyword):
        """Check if keyword appears in content (case-insensitive)"""
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        matches = pattern.findall(content)
        return len(matches) > 0, len(matches)
    
    def check_website(self, site_name, site_url, check_keyword=None, extra_note=None):
        """Check if website content has changed"""
        content = self.fetch_website(site_url)
        if content is None:
            return False
        
        # Remove whitespace for more reliable comparison
        cleaned_content = ' '.join(content.split())
        current_hash = self._get_content_hash(cleaned_content)
        previous_hash = self.state.get(site_name, {}).get('hash')
        
        if previous_hash is None:
            # First time monitoring this site
            self.state[site_name] = {
                'hash': current_hash,
                'last_checked': datetime.now().isoformat(),
                'status': 'monitoring'
            }
            self._save_state()
            logger.info(f"Started monitoring {site_name}")
            
            # Check for keyword on first run
            if check_keyword:
                found, count = self.check_for_keyword(content, check_keyword)
                if found:
                    logger.info(f"Keyword '{check_keyword}' found {count} time(s) on first check")
            
            return False
        
        if current_hash != previous_hash:
            # Website content has changed
            timestamp = datetime.now().isoformat()
            self.state[site_name]['hash'] = current_hash
            self.state[site_name]['last_changed'] = timestamp
            self.state[site_name]['last_checked'] = timestamp
            self._save_state()
            
            message = (
                f"🚨 <b>Website Changed!</b>\n\n"
                f"<b>Site:</b> {site_name}\n"
                f"<b>URL:</b> <a href='{site_url}'>{site_url}</a>\n"
                f"<b>Time:</b> {timestamp}\n\n"
                f"Content has been updated."
            )
            
            # Check for keyword in new content
            if check_keyword:
                found, count = self.check_for_keyword(content, check_keyword)
                if found:
                    message += (
                        f"\n\n⚠️ <b>Keyword Alert!</b>\n"
                        f"Found '<b>{check_keyword}</b>' {count} time(s) in the updated content.\n"
                    )
                    if extra_note:
                        message += f"\n{extra_note}"
            
            logger.info(f"Website {site_name} has changed!")
            self.send_telegram_notification(message)
            return True
        else:
            # No changes
            self.state[site_name]['last_checked'] = datetime.now().isoformat()
            self._save_state()
            logger.info(f"No changes detected for {site_name}")
            return False
    
    def monitor(self, check_interval=300):
        """Start monitoring websites"""
        websites = self.config.get('websites', [])
        
        if not websites:
            logger.error("No websites configured to monitor")
            return
        
        logger.info(f"Starting monitoring of {len(websites)} website(s)")
        logger.info(f"Check interval: {check_interval} seconds")
        
        try:
            while True:
                for site in websites:
                    site_name = site.get('name')
                    site_url = site.get('url')
                    check_keyword = site.get('check_for_keyword')
                    extra_note = site.get('extra_note')
                    
                    if not site_name or not site_url:
                        logger.warning("Invalid site configuration")
                        continue
                    
                    self.check_website(site_name, site_url, check_keyword, extra_note)
                
                logger.info(f"Sleeping for {check_interval} seconds...")
                time.sleep(check_interval)
        
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")


def main():
    """Main entry point"""
    try:
        monitor = WebsiteMonitor('config.json')
        # Check every 5 minutes (300 seconds)
        monitor.monitor(check_interval=300)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
