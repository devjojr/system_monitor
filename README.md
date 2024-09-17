# System Monitor Script

This Python script monitors system resource usage, including CPU, memory, and disk usage, and send alerts via email and SMS when specified thresholds are exceeded. The script also implements logging for monitoring activities.

## Features

- **Monitors System Resources**S:

  - CPU usage
  - Memory usage
  - Disk usage

- **Alert Notifications**
  - Send email and SMS alerts when usage exceeds thresholds.

- **Logging**:
  - Logs system monitoring activities to a file (`monitor_resources.log`)
  - Records warnings when thresholds are exceeded and errors if alerts fail to send.

## Requirements

1. `psutil` library for monitoring system resources.
2. `python-dotenv` package to manage environment variables
3. `Twilio` library for sending SMS alerts.
4. An email account with access to a SMTP server for sending email notifications.
5. Twilio account for SMS alerts.
