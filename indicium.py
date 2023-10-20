import subprocess
import time
import os
import argparse
from time import sleep
import shutil

LOW_BATTERY_THRESHOLD = 20
HIGH_BATTERY_THRESHOLD = 80

# ---------------- Banner ---------------- #

def haxor_print(text, leading_spaces=0):
   text_chars = list(text)
   current, mutated = '', ''

   for i in range(len(text)):
      original = text_chars[i]
      current += original
      mutated += f'\033[1;38;5;82m{text_chars[i].upper()}\033[0m'
      print(f'\r{" " * leading_spaces}{mutated}', end='')
      sleep(0.07)
      print(f'\r{" " * leading_spaces}{current}', end='')
      mutated = current

   print(f'\r{" " * leading_spaces}{text}\n')

def print_banner(): 
   print('\r')
   padding = '  '

   I = [[' ', '┬',' '], [' ', '│', ' '],[' ', '┴', ' ']] 
   N = [['┌','┐','┌'], ['│','│','│'], ['┘','└','┘']]
   D = [[' ','┌', '┬','┐'], [' ',' ', '│','│'], [' ','─', '┴','┘']]
   I2 = [[' ', '┬',' '], [' ', '│', ' '],[' ', '┴', ' ']] 
   C = [['┌', '─','┐'], ['│', ' ',' '], ['└', '─','┘']]
   I3 = [[' ', '┬',' '], [' ', '│', ' '],[' ', '┴', ' ']] 
   U = [['┬', ' ','┬'], ['│', ' ', '│'], ['└', '─','┘']]
   M = [[' ','┌', '┬','┐'], [' ','│', '│','│'], [' ','┴', ' ','┴']]

   banner = [I,N,D,I2,C,I3,U,M]
   final = []
   init_color = 228
   txt_color = init_color
   cl = 0

   for charset in range(0, 3):
      for pos in range(0, len(banner)):
         for i in range(0, len(banner[pos][charset])):
            clr = f'\033[38;5;{txt_color}m'
            char = f'{clr}{banner[pos][charset][i]}'
            final.append(char)
            cl += 50
            txt_color = txt_color + 36 if cl <= 3 else txt_color

         cl = 0

         txt_color = init_color
      init_color += 1

      if charset < 2:
         final.append('\n   ')

   END = '\033[0m'
   print(f"   {''.join(final)}{END}")
   haxor_print('by p3rception', 17)

   # Dynamic horizontal line
   terminal_width = shutil.get_terminal_size().columns
   dynamic_line = '─' * terminal_width
   print(f"{dynamic_line}\n")



# -------------- Main functions -------------- #

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


def is_charging():
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
   print_banner()
   low_battery_threshold = args.low_threshold
   high_battery_threshold = args.high_threshold

   while True:
      battery_level = check_battery()

      timestamp = time.strftime("%H:%M", time.localtime())
      print(f"[{timestamp}] The battery level is {battery_level}%")

      if battery_level is not None:
         if battery_level <= low_battery_threshold and not is_charging():
            display_notification(f"Battery Level Below {low_battery_threshold}%\nCharge the device!")
         elif battery_level >= high_battery_threshold and is_charging():
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