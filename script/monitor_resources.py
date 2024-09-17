import psutil
import os
import smtplib
import logging
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


# resources threshold
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 75
DISK_THRESHOLD = 80


# email info
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))


# Twilio info
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TO_PHONE_NUMBER = os.getenv("TO_PHONE_NUMBER")


# logging setup
LOG_FILE = "monitor_resources.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"  # timestamp - security level - message
)


# twilio client setup
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


cpu_alert_sent = False
memory_alert_sent = False
disk_alert_sent = False


def send_sms(message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        logging.info(f'SMS Alert Sent: {message}')
    except Exception as e:
        logging.error(f"Failed to send SMS: {e}")
        logging.warning(f"Warning: SMS alert failed with error {e}")


def send_email(subject, message):
    try:
        logging.info(f"Preparing to send email alert: {subject}")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            logging.info("Connecting to SMTP Server...")
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            logging.info(f'Email Alert Sent: {subject}')
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        logging.warning(f"Warning: Email alert failed with error {e}")


def monitor_system():
    global cpu_alert_sent, memory_alert_sent, disk_alert_sent

    hostname = os.uname().nodename

    # cpu usage vs threshold
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        if not cpu_alert_sent:
            alert_message = f"High CPU Usage Alert on {hostname}: CPU usage is at {cpu_usage}%"
            logging.warning(f"CPU usage is above threshold: {cpu_usage}%")
            send_email("High CPU Usage Alert", alert_message)
            send_sms(alert_message)
            cpu_alert_sent = True
    else:
        if cpu_alert_sent:
            logging.info(f"CPU usage back to normal: {cpu_usage}%")
            cpu_alert_sent = False

    # memory usage vs threshold
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    if memory_usage > MEMORY_THRESHOLD:
        if not memory_alert_sent:
            alert_message = f"High Memory Usage Alert on {hostname}: Memory usage is at {memory_usage}%"
            logging.warning(f"Memory usage is above threshold: {memory_usage}%")
            send_email("High Memory Usage Alert", alert_message)
            send_sms(alert_message)
            memory_alert_sent = True
    else:
        if memory_alert_sent:
            logging.info(f"Memory usage back to normal: {memory_usage}%")
            memory_alert_sent = False

    # disk usage vs threshold
    disk_info = psutil.disk_usage("/")
    disk_usage = disk_info.percent
    if disk_usage > DISK_THRESHOLD:
        if not disk_alert_sent:
            alert_message = f"High Disk Usage Alert on {hostname}: Disk usage is at {disk_usage}%"
            logging.warning(f"Disk usage is above threshold: {disk_usage}%")
            send_email("High Disk Usage Alert", alert_message)
            send_sms(alert_message)
            disk_alert_sent = True
    else:
        if disk_alert_sent:
            logging.info(f"Disk usage back to normal: {disk_usage}%")
            disk_alert_sent = False


if __name__ == "__main__":
    logging.info(f"Starting System Resource Monitoring on {os.uname().nodename}...")
    monitor_system()
    logging.info("Monitoring Finished")
