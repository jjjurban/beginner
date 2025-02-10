import re
import time

# Sample log file (replace with your actual log file path)
LOG_FILE = "server_logs.txt"
ALERT_THRESHOLD = 5  # Number of failed logins before triggering an alert
CHECK_INTERVAL = 2  # Time in seconds between log checks

# Regular expression to detect failed logins (adjust based on log format)
FAILED_LOGIN_PATTERN = re.compile(r"Failed login from (\d+\.\d+\.\d+\.\d+)")

def monitor_logs():
    failed_attempts = {}
    last_position = 0  # Track last read position in file
    
    print("Monitoring logs for suspicious activity (Real-Time)...")
    
    while True:
        with open(LOG_FILE, "r") as file:
            file.seek(last_position)  # Move to last read position
            lines = file.readlines()
            last_position = file.tell()  # Update last read position
            
            for line in lines:
                match = FAILED_LOGIN_PATTERN.search(line)
                if match:
                    ip = match.group(1)
                    failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
                    
                    if failed_attempts[ip] >= ALERT_THRESHOLD:
                        print(f"[ALERT] Multiple failed logins detected from {ip}")
        
        time.sleep(CHECK_INTERVAL)  # Wait before checking again

if __name__ == "__main__":
    monitor_logs()
