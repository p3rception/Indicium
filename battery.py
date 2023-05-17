import subprocess
import time
import os

LOW_BATTERY_THRESHOLD = 20
HIGH_BATTERY_THRESHOLD = 80


def check_battery():
    """
    Returns the current battery level of the device
    """
    battery_level = int(subprocess.check_output(
        "pmset -g batt | grep -Eo '[0-9]{1,3}%' | awk '{print $1}'", shell=True).decode("utf-8").strip().split("%")[0])
    return battery_level


def is_power_connected():
    """
    Returns True if the device is currently charging, else returns False
    """
    power_status = subprocess.check_output(
        "pmset -g ps", shell=True).decode("utf-8").strip()

    if "AC Power" in power_status:
        return True
    else:
        return False


# The main loop continuously checks the battery level and sends notifications based on the battery status
while True:
    battery_level = check_battery()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{timestamp}] The battery level is {battery_level}%")
    if battery_level <= LOW_BATTERY_THRESHOLD and not is_power_connected():
        os.system(
            "osascript -e 'display notification \"Battery Level Below 20%\nCharge the device!\" with title \"Battery Status\" sound name \"Submarine\"'")
    elif battery_level >= HIGH_BATTERY_THRESHOLD and is_power_connected():
        os.system(
            "osascript -e 'display notification \"Battery Level Above 80%\nUnplug the device!\" with title \"Battery Status\" sound name \"Submarine\"'")
    time.sleep(300)  # Checks every 5 minutes
