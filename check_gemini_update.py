import subprocess
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os

# Configuration
SMTP_SERVER = "smtp.mail.me.com"
SMTP_PORT = 587
SENDER_EMAIL = "gautambiswas2004@icloud.com"
RECEIVER_EMAIL = "gautambiswas2004@gmail.com"
PASSWORD = "jjho-mufs-iyya-nbit"

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gemini_update_check.log")

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def check_for_updates():
    try:
        # Update homebrew first to ensure we have the latest formulae
        log("Updating Homebrew...")
        subprocess.run(["/opt/homebrew/bin/brew", "update"], capture_output=True)
        
        # Check if gemini-cli is outdated
        log("Checking for gemini-cli updates...")
        result = subprocess.run(
            ["/opt/homebrew/bin/brew", "outdated", "--json"], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            log(f"Error running brew outdated: {result.stderr}")
            return None

        outdated_formulae = json.loads(result.stdout).get("formulae", [])
        for formula in outdated_formulae:
            if formula["name"] == "gemini-cli":
                return {
                    "current": formula["installed_versions"][0],
                    "latest": formula["current_version"]
                }
        
        log("gemini-cli is up to date in Homebrew.")
        return None

    except Exception as e:
        log(f"Exception in check_for_updates: {e}")
        return None

def send_email(current_ver, latest_ver):
    subject = "Reminder: Gemini CLI Update Available in Homebrew"
    body = f"""
Hello,

A new version of Gemini CLI is available in Homebrew!

Current version: {current_ver}
Latest version: {latest_ver}

You can update it by running:
brew upgrade gemini-cli

Sent from your automated checker script.
"""

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        log(f"Update notification email sent for version {latest_ver}!")
    except Exception as e:
        log(f"Error sending email: {e}")

if __name__ == "__main__":
    log("Starting Gemini CLI update check...")
    update_info = check_for_updates()
    if update_info:
        log(f"Update found: {update_info['current']} -> {update_info['latest']}")
        send_email(update_info['current'], update_info['latest'])
    else:
        # No update found in Brew yet.
        pass
