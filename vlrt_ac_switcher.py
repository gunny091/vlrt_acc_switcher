import pygetwindow
import pyautogui
import pyperclip
import time
import json

print("Valorant Account Switcher by Chadol27")
print("Version 1.5")
print()

def exit_timeout(text):
  print(text)
  print("This window will be closed in 5 seconds")
  time.sleep(5)
  exit()

def try_to_click_image(path, click=True):
  try:
    location = pyautogui.locateCenterOnScreen(path, grayscale=True, confidence=0.9)
  except pyautogui.ImageNotFoundException:
    return False
  else:
    if click : pyautogui.click(location)
    return True

def try_to_click_images(paths, click=True):
  for path in paths:
    if try_to_click_image(path, click):
      return True
  return False

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
  account_paths = ["./img/account_small.png", "./img/account_big.png"]
  logout_paths = ["./img/logout.png", "./img/logout_hover.png"]
  username_paths = ["./img/username.png", "./img/username_clicked.png"]

  if try_to_click_images(username_paths):
    time.sleep(0.1)
    return
  elif try_to_click_images(account_paths):
    time.sleep(0.1)
    try_to_click_images(logout_paths)
    time.sleep(3)
    if try_to_click_images(username_paths):
     time.sleep(0.1)
     return
    else:
      raise Exception("Image not found")
  else:
    raise Exception("Image not found")

def focus_window(name):
  try:
    window = pygetwindow.getWindowsWithTitle(name)[0]
    if window:
      window.activate()
      return True
    else:
      return False
  except:
    return False

def ready_riot_client():
  # Check if window is running
  for _ in range(3):
    if (focus_window("Riot Client")):
      time.sleep(0.5)
      return
    time.sleep(1)
  exit_timeout("Please launch Riot Client")


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

  stopmessage = "focusing Riot Client window"
  ready_riot_client()

  stopmessage = "getting ready to input"
  input_ready()

  stopmessage = "inputing"
  input_idpwd(*idpwd)
except Exception as e:
  exit_timeout("Error while " + stopmessage + ": " + str(e)) 
else:
  exit_timeout("Success")