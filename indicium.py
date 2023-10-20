import subprocess
import time
import os
import argparse

LOW_BATTERY_THRESHOLD = 20
HIGH_BATTERY_THRESHOLD = 80


def check_battery():
   """
   Returns the current battery level of the device
   """
   try:
      output = subprocess.check_output(
         "pmset -g batt | grep -Eo '[0-9]{1,3}%' | awk '{print $1}'", shell=True).decode("utf-8").strip().split("%")[0]
      battery_level = int(output)
      return battery_level
   except subprocess.CalledProcessError as e:
      print(f"Error checking battery level: {e}")
      return None


def is_power_connected():
   """
   Returns True if the device is currently charging, else returns False
   """
   try:
      power_status = subprocess.check_output(
         "pmset -g ps", shell=True).decode("utf-8").strip()

      if "AC Power" in power_status:
         return True
      else:
         return False
   except subprocess.CalledProcessError as e:
      print(f"Error checking power status: {e}")
      return None


def display_notification(message):
   """
   Displays a notification with the given message
   """
   try:
      os.system(
         f"osascript -e 'display notification \"{message}\" with title \"Battery Status\" sound name \"Submarine\"'")
   except OSError as e:
      print(f"Error displaying notification: {e}")


def main(args):
   low_battery_threshold = args.low_threshold
   high_battery_threshold = args.high_threshold

   while True:
      battery_level = check_battery()

      timestamp = time.strftime("%H:%M", time.localtime())
      print(f"[{timestamp}] The battery level is {battery_level}%")

      if battery_level is not None:
         if battery_level <= low_battery_threshold and not is_power_connected():
            display_notification(f"Battery Level Below {low_battery_threshold}%\nCharge the device!")
         elif battery_level >= high_battery_threshold and is_power_connected():
            display_notification(f"Battery Level Above {high_battery_threshold}%\nUnplug the device!")

      time.sleep(300)  # Checks every 5 minutes

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="Battery monitoring and notification script")
   parser.add_argument("-l", "--low_threshold", type=int, default=20, help="Low battery threshold")
   parser.add_argument("-ht", "--high_threshold", type=int, default=80, help="High battery threshold")
   args = parser.parse_args()
   try:
      main(args)
   except KeyboardInterrupt:
      print("\nIndicium was terminated.")