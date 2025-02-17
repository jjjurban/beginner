import re

# Define suspicious patterns (basic example)
suspicious_patterns = [
    r'failed login',
    r'error',
    r'unauthorized access',
    r'root access',
    r'brute force',
    r'permission denied'
]

def detect_anomalies(log_file, output_file):
    with open(log_file, 'r') as f:
        logs = f.readlines()
    
    flagged_logs = []
    for line in logs:
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in suspicious_patterns):
            flagged_logs.append(line)
    
    with open(output_file, 'w') as f:
        f.writelines(flagged_logs)
    
    print(f"Detected {len(flagged_logs)} suspicious log entries. See {output_file}")

# Example usage
detect_anomalies('system_logs.txt', 'flagged_logs.txt')
