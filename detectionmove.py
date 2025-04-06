import pyautogui
import cv2
import numpy as np
import time as tm
import keyboard
import pydirectinput
import threading
import matplotlib.pyplot as plt
import pyWinhook as ph
import pythoncom

status_engine_read = False
waiting_active = False
prev_image = None

def start_rad_engine():
    global status_engine_read
    global waiting_active
    status_engine_read = not status_engine_read
    waiting_active = False
    print(f"Automation {'started' if status_engine_read else 'stopped'}")

def interrupt():
    global waiting_active
    print("off engine read")
    waiting_active = True
    
def custom_sleep(duriton): 
    global waiting_active
    for z in range(duriton):
        if not waiting_active:
            return
        tm.sleep(1)    

def read_number():
    global status_engine_read
    global prev_image
    global waiting_active
     
    if not status_engine_read:
        return
    
    region = (1182, 1005,40, 40) 
    
    while True:
        
        if waiting_active:
            print("waiting active")
            custom_sleep(600)
        
        screenshot = pyautogui.screenshot(region=region)
        current_frame = np.array(screenshot)
        
        gray = cv2.cvtColor(current_frame, cv2.COLOR_RGB2GRAY)
        gray_frame = cv2.medianBlur(gray, 5)

        if prev_image is not None:
            # Lakukan perbandingan dengan frame sebelumnya
            diff = cv2.absdiff(prev_image, gray_frame)
            _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
            if cv2.countNonZero(thresh) > 0:
                print("Gerakan terdeteksi")
            else:
                print("Tidak ada gerakan")
                waiting_active = True
                status_engine_read = False
                tm.sleep(0.6)
                pydirectinput.press('9')
                continue

        prev_image = gray_frame
        tm.sleep(0.8)


def OnKeyboardEvent(event):
    # Deteksi 0
    if event.Key == '0':
        start_rad_engine()
        print("lol")
    
    # Hotkey tambahan untuk keluar (Alt+Q)
    elif event.Key == '8':
        interrupt()
    
    elif event.Key == 'Q' and event.Alt:
        return False  # Menghentikan hook
    return True  # Melanjutkan proses event

def start_hook():
    hook_manager = ph.HookManager()
    hook_manager.KeyDown = OnKeyboardEvent
    hook_manager.HookKeyboard()
    pythoncom.PumpMessages()

# Jalankan hook keyboard di thread terpisah
hook_thread = threading.Thread(target=start_hook)
hook_thread.daemon = True  # Thread akan berhenti saat program utama berhenti
hook_thread.start()

print("start engine read")

while True:
    read_number()
    tm.sleep(0.2)