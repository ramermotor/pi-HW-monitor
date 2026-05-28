# pi-HW-monitor

A simple script to display basic Raspberry Pi stats on an I2C 16x2 LCD screen (using a PCF8574 backpack). 

It loops through CPU usage/temps, RAM usage, and disk space without making the screen flicker like crazy. It also has a built-in timer that kills the bright LCD backlight at night so it doesn't light up the whole room, though it keeps tracking stats in the background.

## Hardware Connections
Wire your LCD backpack to the Pi's GPIO pins:
* **GND** -> Pin 6 (GND)
* **VCC** -> Pin 4 (5V)
* **SDA** -> Pin 3 (SDA)
* **SCL** -> Pin 5 (SCL)

## Quick Start

### 1. Turn on I2C
Run `sudo raspi-config`, go to **Interface Options**, enable **I2C**, and reboot.

### 2. Install dependencies
```bash
sudo apt update
sudo apt install python3-pip i2c-tools
pip3 install RPLCD psutil
```

### 3. Check your I2C address
Run `i2cdetect -y 1`. It will usually show up as `0x27` or `0x3f`. Make sure the address inside the script matches whatever your terminal outputs.

## Running it as a service
To make it launch automatically on boot and restart if it ever crashes, wrap it in a systemd service.

1. Open a new service file:
```bash
sudo nano /etc/systemd/system/pi-lcd.service
```

2. Paste this configuration (fix the paths to match your actual files):
```ini
[Unit]
Description=Pi LCD Hardware Monitor
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/pi-HW-monitor
ExecStart=/usr/bin/python3 monitor.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Start it up:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pi-lcd.service
sudo systemctl start pi-lcd.service
```

## Logs
If something goes wrong or you need to debug line breaks, check the systemd output:
```bash
journalctl -u pi-lcd.service -f
```

## License
GPLv3 (Keep it open source).
