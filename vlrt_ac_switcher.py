import pygetwindow
import psutil
import pyautogui
import pyperclip
import time
import json

print("Valorant Account Switcher by Chadol27")
print("Version 1.1")
print()

def exit_timeout(text):
  print(text)
  print("This window will be closed in 5 seconds")
  time.sleep(5)
  exit()

def load_account(path):
  # 계정 정보 불러오기
  try:
    with open(path, "r") as f:
      accounts = json.load(f)
      if type(accounts) != dict:
        raise Exception
  except:
    exit_timeout("Error while read accounts")

  # 계정이가 없어요
  keys = accounts.keys()
  if (len(keys) == 0):
    exit_timeout("No account")

  # 계정 표시
  print("Select an account")
  for index, account in enumerate(keys):
    print(f"{index}: {account}")

  # 계정 골라
  while True:
    user_input = input("> ")
    if not user_input.isnumeric() : continue
    user_input_number = int(user_input)
    if not 0 <= user_input_number <= len(keys) : continue

    selected = list(keys)[user_input_number]
    break

  # 아이디 비번 추출
  id = accounts[selected][0]
  pwd = accounts[selected][1]
  return id, pwd


def input_ready():
  # 프로세스 실행 확인
  def check_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
      if proc.info['name'] == process_name:
        return True
    return False

  if not check_process_running("Riot Client.exe"):
    exit_timeout("Please launch Riot Client")

  # 윈도우 실행 확인
  window = pygetwindow.getWindowsWithTitle('Riot Client')[0]
  if window:
    window.activate()
  else:
    exit_timeout("Please launch Riot Client UI")

  image_hangul_path = "./username_hangul.png"

  time.sleep(1)

  # 계정이름 위치 찾기
  try:
    location = pyautogui.locateCenterOnScreen(image_hangul_path,grayscale=True)
  except:
    exit_timeout("Can't find the user name button")

  pyautogui.click(location)
  time.sleep(0.1)

def input_idpwd(id, pwd):
  # 아이디 입력
  pyperclip.copy(id)
  time.sleep(0.1)

  pyautogui.hotkey("ctrl", "v")
  pyautogui.press("tab")

  # 비번 입력
  pyperclip.copy(pwd)
  time.sleep(0.1)

  pyautogui.hotkey("ctrl", "v")
  
  # 엔터

  pyautogui.press("enter")

try:
  stopmessage = "loading and selecting account"
  idpwd = load_account("./accounts.json")

  stopmessage = "getting ready to input"
  input_ready()
  
  stopmessage = "inputing"
  input_idpwd(*idpwd)
except:
  exit_timeout("Error while " + stopmessage)
else:
  exit_timeout("Success")