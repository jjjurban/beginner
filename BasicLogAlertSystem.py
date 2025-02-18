import re
import time
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='Config_BasicLogalertSys.env')

# Sample log file (replace with your actual log file path)
LOG_FILE = "server_logs.txt"
ALERT_THRESHOLD = 3  # Number of failed logins before triggering an alert
CHECK_INTERVAL = 2  # Time in seconds between log checks

# Email configuration (Loaded from .env)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Regular expression to detect failed logins (adjust based on log format)
FAILED_LOGIN_PATTERN = re.compile(r"Failed login from (\d+\.\d+\.\d+\.\d+)")

def send_email_alert(ip):
    """Sends an email alert when a suspicious login is detected."""
    subject = "[ALERT] Suspicious Login Detected"
    body = f"Multiple failed logins detected from {ip}. Immediate action is recommended."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure connection
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"[EMAIL SENT] Alert sent to {EMAIL_RECEIVER} for {ip}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def monitor_logs():
    failed_attempts = {}
    
    # Open the log file in read mode and set the pointer to the end of the file
    with open(LOG_FILE, "r") as file:
        file.seek(0, os.SEEK_END)  # Start reading from the end of the file
        
        print("Monitoring logs for suspicious activity (Real-Time)...")
        
        while True:
            # Read the next line from the file
            line = file.readline()
            
            if not line:
                # If no new line, wait and check again
                time.sleep(CHECK_INTERVAL)
                continue
            
            # Search for failed login attempts
            match = FAILED_LOGIN_PATTERN.search(line)
            if match:
                ip = match.group(1)
                failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
                
                if failed_attempts[ip] >= ALERT_THRESHOLD:
                    print(f"[ALERT] Multiple failed logins detected from {ip}")
                    send_email_alert(ip)  # Send email alert

if __name__ == "__main__":
    monitor_logs()
