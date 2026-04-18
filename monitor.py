import os
import time
from datetime import datetime

# Store previous status to avoid repeated alerts
previous_status = {}

# Function to ping a host
def ping(host):
    response = os.system(f"ping -n 1 {host} > nul")  # Windows
    return response == 0

# Load hosts
def load_hosts():
    with open("hosts.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

# Log to file
def log_status(host, status):
    with open("log.txt", "a") as log:
        log.write(f"{datetime.now()} - {host} - {status}\n")

# Alert system
def alert(host):
    print(f"\n🚨 ALERT: {host} is DOWN!\n")
    os.system("echo \a")  # Beep sound (works in Windows)

# Monitor function
def monitor_hosts():
    global previous_status
    hosts = load_hosts()

    print("Starting Network Monitoring with Alerts...\n")

    while True:
        print("=" * 50)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

        for host in hosts:
            is_up = ping(host)
            status = "UP ✅" if is_up else "DOWN ❌"

            print(f"{host:20} : {status}")
            log_status(host, status)

            # Alert only when status changes from UP → DOWN
            if host in previous_status:
                if previous_status[host] == True and not is_up:
                    alert(host)

            previous_status[host] = is_up

        time.sleep(10)


if __name__ == "__main__":
    monitor_hosts()