import pygetwindow
import psutil
import pyautogui
import pyperclip
import time
import json

print("Valorant Account Switcher by Chadol27")
print("Version 1.2")
print()

def exit_timeout(text):
  print(text)
  print("This window will be closed in 5 seconds")
  time.sleep(5)
  exit()

def load_account(path):
  # Load account information
  try:
    with open(path, "r") as f:
      accounts = json.load(f)
      if type(accounts) != dict:
        raise Exception
  except:
    exit_timeout("Error while read accounts")

  # No accounts
  keys = accounts.keys()
  if (len(keys) == 0):
    exit_timeout("No account")

  # Display accounts
  print("Select an account")
  for index, account in enumerate(keys):
    print(f"{index}: {account}")

  # Select account
  while True:
    user_input = input("> ")
    if not user_input.isnumeric() : continue
    user_input_number = int(user_input)
    if not 0 <= user_input_number <= len(keys) : continue

    selected = list(keys)[user_input_number]
    break

  # Extract ID and password
  id = accounts[selected][0]
  pwd = accounts[selected][1]
  return id, pwd


def input_ready():
  # Check if process is running
  def check_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
      if proc.info['name'] == process_name:
        return True
    return False

  if not check_process_running("Riot Client.exe"):
    exit_timeout("Please launch Riot Client")

  # Check if window is running
  window = pygetwindow.getWindowsWithTitle('Riot Client')[0]
  if window:
    window.activate()
  else:
    exit_timeout("Please launch Riot Client UI")

  username_path = "./username_hangul.png"
  account_path = "./account.png"
  logout_path = "./logout.png"

  time.sleep(0.2)

  # Logout if logged in
  try:
    account_location = pyautogui.locateCenterOnScreen(account_path,grayscale=True, confidence=0.8)
  except:
    pass
  else:
    pyautogui.click(account_location)
    time.sleep(0.1)
    try:
      logout_location = pyautogui.locateCenterOnScreen(logout_path,grayscale=True, confidence=0.8)
    except:
      pass
    else:
      pyautogui.click(logout_location)
      time.sleep(2)

  time.sleep(0.1)

  # Find username location
  try:
    username_location = pyautogui.locateCenterOnScreen(username_path,grayscale=True, confidence=0.8)
  except pyautogui.ImageNotFoundException:
    exit_timeout("Can't find the user name button")

  pyautogui.click(username_location)
  time.sleep(0.1)

def input_idpwd(id, pwd):
  # Input ID
  pyperclip.copy(id)
  time.sleep(0.1)

  pyautogui.hotkey("ctrl", "v")
  pyautogui.press("tab")

  # Input password
  pyperclip.copy(pwd)
  time.sleep(0.1)

  pyautogui.hotkey("ctrl", "v")
  
  # Press enter
  pyautogui.press("enter")

try:
  stopmessage = "loading and selecting account"
  idpwd = load_account("./accounts.json")

  stopmessage = "getting ready to input"
  input_ready()

  stopmessage = "inputing"
  input_idpwd(*idpwd)
except Exception as e:
  exit_timeout("Error while " + stopmessage) 
else:
  exit_timeout("Success")