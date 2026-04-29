import os
import random
import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

# Path to your consolidated env
load_dotenv('.env')

RECIPIENT_EMAIL = "gautambiswas2004@icloud.com"

def log_activity(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    with open("daily_news_log.log", "a") as f:
        f.write(log_line + "\n")
    return log_line

def send_status_email(status, detail):
    # Note: iCloud requires an "App-Specific Password" for SMTP
    # Ensure EMAIL_PASSWORD is set in your replate/.env
    sender = os.getenv('EMAIL_USER', RECIPIENT_EMAIL)
    password = os.getenv('EMAIL_PASSWORD')
    
    if not password:
        log_activity("SKIPPED: Email not sent (EMAIL_PASSWORD missing in .env)")
        return

    msg = MIMEText(f"Replate System Sync Result:\n\nStatus: {status}\nDetail: {detail}\nTime: {datetime.now()}")
    msg['Subject'] = f"Replate Sync: {status}"
    msg['From'] = sender
    msg['To'] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP('smtp.mail.me.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, [RECIPIENT_EMAIL], msg.as_string())
        log_activity(f"SUCCESS: Status email sent to {RECIPIENT_EMAIL}")
    except Exception as e:
        log_activity(f"ERROR: Failed to send status email. {e}")

def run_masked_task():
    # Random delay for organic appearance
    delay = random.randint(0, 300) # Reduced for testing, can be increased
    log_activity(f"System Check initiated. Organic delay: {delay}s")
    time.sleep(delay)

    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    if not url or not key:
        err = "Environment variables missing."
        log_activity(f"CRITICAL: {err}")
        send_status_email("FAILURE", err)
        return

    headers = {"apikey": key, "Authorization": f"Bearer {key}"}

    try:
        # Simulate app activity
        response = requests.get(f"{url}/rest/v1/available_tasks?limit=1", headers=headers, timeout=15)
        
        if response.status_code == 200:
            msg = "DB Connectivity verified. Sync complete."
            log_activity(msg)
            send_status_email("SUCCESS", msg)
        else:
            msg = f"Unexpected response code: {response.status_code}"
            log_activity(msg)
            send_status_email("WARNING", msg)
            
    except Exception as e:
        msg = f"Network sync failed. {e}"
        log_activity(f"ERROR: {msg}")
        send_status_email("FAILURE", msg)

if __name__ == "__main__":
    run_masked_task()
