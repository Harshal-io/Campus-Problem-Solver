import os
from datetime import datetime

# Simple notifier implementation
def notify(problem_id, department, category):
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, 'notifications.log')
    
    timestamp = datetime.now().isoformat()
    log_msg = f"[{timestamp}] ID: {problem_id} | Category: {category} | Assigned To: {department}"
    
    # Write to log file
    with open(log_path, 'a') as f:
        f.write(log_msg + '\n')
        
    # Print to console
    print(log_msg)
    
    # Optional SMTP handling could go here
    smtp_host = os.environ.get("SMTP_HOST")
    if smtp_host:
        print("Sending email via SMTP (mocked)")
