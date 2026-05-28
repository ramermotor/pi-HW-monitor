import time
import psutil
import subprocess
import datetime
from RPLCD.i2c import CharLCD

# Initialize LCD (change address to 0x27 or 0x3f as needed)
lcd = CharLCD('PCF8574', 0x3f, auto_linebreaks=True)

# --------- Configurations ---------
OFF_HOUR = 22  # 10:00 PM (Backlight turns off)
ON_HOUR = 6    # 6:00 AM (Backlight turns on)

# --------- Data Functions ---------

def get_cpu_temp():
    try:
        out = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
        return out.replace("temp=", "").strip()
    except:
        return "N/A"

def get_ram_usage():
    mem = psutil.virtual_memory()
    used = mem.used // (1024 * 1024)
    total = mem.total // (1024 * 1024)
    return f"{used}/{total}MB"

def get_disk_usage():
    disk = psutil.disk_usage('/')
    used = disk.used // (1024 * 1024 * 1024)
    total = disk.total // (1024 * 1024 * 1024)
    return f"{used}/{total}GB"

# --------- Display Loop ---------

try:
    page = 0
    refresh_interval = 0.5  # Check stats twice a second
    page_duration = 5       # Stay on each page for 5 seconds
    page_refreshes = int(page_duration / refresh_interval)

    while True:
        # 1. Backlight Schedule Check
        current_hour = datetime.datetime.now().hour
        if OFF_HOUR > ON_HOUR:
            is_dark_hours = (current_hour >= OFF_HOUR or current_hour < ON_HOUR)
        else:
            is_dark_hours = (OFF_HOUR <= current_hour < ON_HOUR)

        lcd.backlight_enabled = not is_dark_hours

        # 2. Page Transition Clear
        lcd.clear()
        
        for _ in range(page_refreshes):
            lcd.home()  # Overwrites text without flickering

            if page == 0:
                # Page 1: CPU Performance Data
                cpu_temp = get_cpu_temp()
                cpu_usage = psutil.cpu_percent()
                lcd.write_string(f"CPU Temp: {cpu_temp}  \r\n")
                lcd.write_string(f"CPU Load: {cpu_usage:.0f}%   ")

            elif page == 1:
                # Page 2: System Memory Allocation
                ram_usage = get_ram_usage()
                lcd.write_string("RAM Usage:      \r\n")
                lcd.write_string(f"{ram_usage}   ")

            elif page == 2:
                # Page 3: Drive Storage
                disk_usage = get_disk_usage()
                lcd.write_string("Disk Space:     \r\n")
                lcd.write_string(f"{disk_usage}   ")

            time.sleep(refresh_interval)

        page = (page + 1) % 3  # Cycle through our 3 hardware screens

except KeyboardInterrupt:
    lcd.clear()
