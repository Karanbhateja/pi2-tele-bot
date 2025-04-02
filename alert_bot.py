import time
import psutil
import requests
import subprocess

# Telegram Bot configuration – replace with your own values.
BOT_TOKEN = "api_token"
CHAT_ID = "chat_id"

# Thresholds
TEMP_THRESHOLD = 55    # Temperature in °C
RAM_THRESHOLD = 65     # RAM usage in percent
CPU_THRESHOLD = 85     # CPU usage in percent

# Cooldown period in seconds (e.g., 300 seconds = 5 minutes)
COOLDOWN = 150

# Dictionary to store the last alert time for each metric
last_alert = {"temp": 0, "ram": 0, "cpu": 0}

def send_message(text):
    """Send a message using Telegram Bot API."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def get_temp():
    """Fetch Raspberry Pi temperature from /sys/class/thermal/thermal_zone0/temp."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            temp_milli = int(file.read().strip())
            temp_celsius = temp_milli / 1000.0  # Convert from millidegrees
            return temp_celsius
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return 0


def check_metrics():
    """Check system metrics and send alerts if thresholds are exceeded."""
    current_time = time.time()

    # Check temperature
    temp = get_temp()
    if temp > TEMP_THRESHOLD and (current_time - last_alert["temp"]) >= COOLDOWN:
        send_message(f"Temperature: {temp:.1f}°C.\nDo you have any plans to cook meals on my processor ? If Not, then turn the FUCKING FAN ON!!")
        last_alert["temp"] = current_time

    # Check RAM usage
    ram = psutil.virtual_memory().percent
    if ram > RAM_THRESHOLD and (current_time - last_alert["ram"]) >= COOLDOWN:
        send_message(f"RAM usage: {ram:.1f}% \nIf you forgot it by any chance then let me FUCKING REMIND YOU!, I only have 900 MB of RAM")
        last_alert["ram"] = current_time

    # Check CPU usage (using a 1-second interval for measurement)
    cpu = psutil.cpu_percent(interval=1)
    if cpu > CPU_THRESHOLD and (current_time - last_alert["cpu"]) >= COOLDOWN:
        send_message(f"CPU usage: {cpu:.1f}% \nWhat are you trying to run on me ? I am a Raspberry Pi not a FUCKING SUPERCOMPUTER!!")
        last_alert["cpu"] = current_time

if __name__ == "__main__":
    while True:
        check_metrics()
        # Sleep for 2 seconds before checking again.
        time.sleep(2)
