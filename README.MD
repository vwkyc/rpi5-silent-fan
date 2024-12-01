# Raspberry Pi 5 Fan Control

This guide will help you set up automatic fan control for your Raspberry Pi 5.

## Setup Instructions

1. **Copy your working script to a system location:**
    ```bash
    sudo cp fanspeed.py /usr/local/bin/fan_control.py
    sudo chmod +x /usr/local/bin/fan_control.py
    ```

2. **Create the systemd service file:**
    ```bash
    sudo nano /etc/systemd/system/fan-control.service
    ```
    Copy and paste the following service configuration into this file:
    ```plaintext
    [Unit]
    Description=Raspberry Pi 5 Fan Control Service
    After=multi-user.target

    [Service]
    ExecStart=/usr/bin/python3 /usr/local/bin/fan_control.py
    Restart=always
    RestartSec=10
    User=root
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=fan-control

    [Install]
    WantedBy=multi-user.target
    ```

3. **Enable and start the service:**
    ```bash
    sudo systemctl enable fan-control.service
    sudo systemctl start fan-control.service
    ```

4. **Verify that it's running:**
    ```bash
    sudo systemctl status fan-control.service
    ```

## Customizing Fan Behavior

You can customize the fan behavior if needed. Here are some options:

1. **To make the fan quieter, you can adjust the temperature thresholds in the script. Open the script:**
    ```bash
    sudo nano /usr/local/bin/fan_control.py
    ```

2. **Find the `calculate_fan_speed` function and modify the thresholds as needed. For example, for an even quieter operation:**
    ```python
    def calculate_fan_speed(temp):
    ```

3. **After making any changes, restart the service:**
    ```bash
    sudo systemctl restart fan-control.service
    ```

## Additional Commands

1. **To view the logs of the fan control service:**
    ```bash
    journalctl -u fan-control.service
    ```

2. **To stop the service temporarily:**
    ```bash
    sudo systemctl stop fan-control.service
    ```

3. **To disable the service from starting at boot:**
    ```bash
    sudo systemctl disable fan-control.service
    ```