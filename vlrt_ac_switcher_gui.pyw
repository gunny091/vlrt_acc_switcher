import tkinter as tk
from tkinter import font
import json
import asyncio
import os
import pyautogui
import pyperclip
import pygetwindow

# 창 준비
root = tk.Tk()

# 계정 설정 파일
accounts_path = "./accounts.json"

# 색상들
COLOR_RED = "LightCoral"
COLOR_LIGHTBLUE = "SkyBlue"
COLOR_BLUE = "MediumBlue"
COLOR_GREEN = "MediumSeaGreen"
COLOR_TITLE = "SteelBlue"

# 폰트 이지하게 만들기
def get_font(family="Segoe UI", size=12, **kwargs):
  return font.Font(family=family, size=size, **kwargs)

# 라벨 이지하게 만들기
def printlabel(text, font=get_font(), pady=5, **kwargs):
  label = tk.Label(root, text=text, font=font, **kwargs)
  label.pack(pady=pady)
  return label

# 창, 제목 버튼관련 설정
def window_and_title_buttons():
  root.title("Valorant Account Switcher")
  root.geometry("400x600")
  root.resizable(False, True)

  # 제목
  printlabel("Valorant Account Switcher\nv2.2 by chadol27", font=get_font(size=16, weight="bold"), pady=10, fg=COLOR_TITLE)

  make_log()

  # 버튼들
  def end():
    root.quit()
    asyncio.get_event_loop().stop()
  exit_button = tk.Button(text="Exit", font=get_font(), command=end, bg=COLOR_RED)
  exit_button.pack(padx=5, pady=5)

  accounts_file_button = tk.Button(text="Open Accounts File", font=get_font(), command=acc_file_btn_handler)
  accounts_file_button.pack(padx=5, pady=5)

# 계정 설정 파일 열기
def acc_file_btn_handler():
  if not os.path.exists(accounts_path):
    with open(accounts_path, 'w') as f:
      json.dump({}, f)
  os.system("start " + accounts_path)
  log("Account File Opened", fg=COLOR_GREEN)

# 로그 라벨 만들기
log_label = tk.Label()
def make_log():
  global log_label
  log_label = printlabel("<LOG>")

# 로그 라벨 텍스트 변경
def log(text, fg="black", **kwargs):
  log_label.config(text=text, fg=fg, **kwargs)

# 계정 정보 로딩하고 관련 버튼 만들기
accounts = dict()
def load_account_and_button():
  global accounts
  # 계정 정보 로딩
  try:
    with open(accounts_path, "r") as f:
      accounts = json.load(f)
      if type(accounts) != dict:
        raise Exception
  except:
    log("Error while read accounts file", fg=COLOR_RED)
    return

  # 계정이가 없어요
  if (len(accounts.keys()) == 0):
    log("No account", fg=COLOR_RED)
    return

  # 계정 표시
  make_dropdown()
  make_login_button()

# 드롭다운 메뉴 만들기
account_select_var = tk.StringVar(root)
def make_dropdown():
  keys = accounts.keys()
  account_select_var.set(list(keys)[0])

  printlabel("Select Account:")
  dropdown = tk.OptionMenu(root, account_select_var, *keys)
  dropdown.config(font=get_font())
  dropdown.pack()
  log("Account Loaded", fg=COLOR_GREEN)

is_logging_in = False
# 버튼 만들기
def make_login_button():
  def loginbutton_handler():
    global is_logging_in
    if is_logging_in:
      log("Already logging in", fg=COLOR_RED)
      return
    try:
      is_logging_in = True
      asyncio.create_task(letsgo_login(*accounts.get(account_select_var.get())))
    except:
      log("Error loading account ID/PWD", fg=COLOR_RED)
  loginbutton = tk.Button(root, text="Log In", command=loginbutton_handler, font=get_font(), bg=COLOR_LIGHTBLUE)
  loginbutton.pack(padx=5,pady=5)

# 화면에서 이미지 찾아 클릭
def try_to_click_image(path, click=True):
  try:
    location = pyautogui.locateCenterOnScreen(path, grayscale=True, confidence=0.9)
  except pyautogui.ImageNotFoundException:
    return False
  else:
    if click : pyautogui.click(location)
    return True

# 여러개
def try_to_click_images(paths, click=True):
  for path in paths:
    if try_to_click_image(path, click):
      return True
  return False

# 윈도우 포커싱
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

# 라이엇 클라이언트 준비시ㅕㅋ
async def ready_riot_client():
  # Check if window is running
  for _ in range(3):
    if (focus_window("Riot Client")):
      await asyncio.sleep(0.5)
      return True
    await asyncio.sleep(0.5)
  log("Please launch Riot Client", fg=COLOR_RED)
  return False

# 아이디 비번 깔쌈하게 입력할 수 있게 대기
async def input_ready():
  account_paths = ["./img/account_small.png", "./img/account_big.png"]
  logout_paths = ["./img/logout.png", "./img/logout_hover.png"]
  username_paths = ["./img/username.png", "./img/username_clicked.png"]

  if try_to_click_images(username_paths):
    await asyncio.sleep(0.1)
    return True
  elif try_to_click_images(account_paths):
    await asyncio.sleep(0.1)
    try_to_click_images(logout_paths)
    await asyncio.sleep(3)
    if try_to_click_images(username_paths):
     await asyncio.sleep(0.1)
     return True
  log("Error getting ready to input", fg=COLOR_RED)
  return False

# 깔쌈한 입력
async def input_idpwd(id, pwd):
  # Input ID
  pyperclip.copy(id)
  await asyncio.sleep(0.1)

  pyautogui.hotkey("ctrl", "v")
  pyautogui.press("tab")

  # Input password
  pyperclip.copy(pwd)
  await asyncio.sleep(0.1)

  pyautogui.hotkey("ctrl", "v")
  
  # Press enter
  pyautogui.press("enter")

# 로그인 시도
async def letsgo_login(id, pwd):
  global is_logging_in
  try:
    log("Loading Riot Client...", fg=COLOR_BLUE)
    if not await ready_riot_client(): return
    log("Getting ready to input...", fg=COLOR_BLUE)
    if not await input_ready(): return
    log("Inputing...", fg=COLOR_BLUE)
    await input_idpwd(id, pwd)
  except Exception as e:
    print(e)
  else:
    log("Success", fg=COLOR_GREEN)
  finally:
    is_logging_in = False

# 실행
window_and_title_buttons()
load_account_and_button()

# 메인루프
async def event_loop():
  while True:
    root.update()
    await asyncio.sleep(1/60)

# (오류) 저기 꺼져
try:
  asyncio.run(event_loop())
except RuntimeError:
  pass