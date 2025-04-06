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
status_running = False
status_detection = False
status_figth = False
status_bottom = False
status_fish = False
prev_image = None

def start_rad_engine():
    global status_engine_read
    status_engine_read = not status_engine_read
    print(f"Automation {'started' if status_engine_read else 'stopped'}")

def toggle():
    global status_running
    status_running = not status_running
    print(f"Automation {'started' if status_running else 'stopped'}")

def start():
    global status_detection
    status_detection = not status_detection
    print(f"Detection {'started' if status_detection else 'stopped'}")
    
def fight():
    global status_figth
    global status_fish
    status_figth = False
    status_fish = False
    pydirectinput.press('8')
    print("status figth : ", status_figth)

def custom_sleep(duriton): 
    global status_figth
    for z in range(duriton):
        if not status_figth:
            return
        tm.sleep(1)
        
def custom_sleep_read(duriton): 
    global status_fish
    for z in range(duriton):
        if status_fish:
            return
        tm.sleep(1)
        
def engine_read():
    while True:
        read_number()
        tm.sleep(0.5)


def read_number():
    global status_engine_read
    global prev_image
     
    if not status_engine_read:
        return
    
    region = (1182, 1005,40, 40) 
    
    while True:
        
        if not status_engine_read:
            prev_image = None
            return
        
        screenshot = pyautogui.screenshot(region=region)
        current_frame = np.array(screenshot)
        
        gray = cv2.cvtColor(current_frame, cv2.COLOR_RGB2GRAY)
        gray_frame = cv2.medianBlur(gray, 5)

        if prev_image is not None:
            # Lakukan perbandingan dengan frame sebelumnya
            diff = cv2.absdiff(prev_image, gray_frame)
            _, thresh = cv2.threshold(diff, 70, 255, cv2.THRESH_BINARY)
            if cv2.countNonZero(thresh) > 0:
                print("Gerakan terdeteksi")
            else:
                print("Tidak ada gerakan")
                print("mematikan engine read")
                status_engine_read = False
                custom_sleep_read(3)
                pydirectinput.press('9')
                return 

        prev_image = gray_frame
        tm.sleep(0.8)

def create_tracker_screen():
    fgbg = cv2.createBackgroundSubtractorMOG2()

    # region = (x, y, width, height)  # Tentukan area yang ingin di-screenshot
    region = (1182, 1005,40, 40)  # Tentukan area yang ingin di-screenshot
    screenshot = pyautogui.screenshot(region=region)
    

    # Konversi screenshot ke format OpenCV (BGR)
    image = np.array(screenshot)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.medianBlur(gray, 5)

    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    fgmask = fgbg.apply(gray)
    plt.imshow(gray)
    plt.axis('off')
    plt.show()



# def detection_bar():
#     lower_red = np.array([0,120,70])
#     upper_red = np.array([10,255,255])
    

def detection_symbol():
    global status_detection
    global status_running
    global status_figth
    global status_bottom
    global status_fish
    
    if not status_detection:
        return
    
    template = cv2.imread("image.png", 0)  # Template dalam grayscale
    template_font = cv2.imread("font.jpg", 0)
    template_height, template_width = template_font.shape

    
    region = (500, 820, 250, 250)  # Tentukan area (koordinat kiri atas dan ukuran)
    while status_detection:
        if status_figth:
            print("sedang figther", status_figth)
            custom_sleep(600)
            continue
            
        screenshot = pyautogui.screenshot(region=region)
        gray_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        
        result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        _, binary_frame = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
        result_font = cv2.matchTemplate(binary_frame, template_font, cv2.TM_CCOEFF_NORMED)
        min_val_font, max_val_font, min_loc_font, max_loc_font = cv2.minMaxLoc(result_font)


        threshold = 0.8
        if max_val >= threshold:
            if status_running:
                pydirectinput.keyDown('alt')
                pydirectinput.press('t')
                tm.sleep(0.1)
                pydirectinput.press('r')
                pydirectinput.keyUp('alt')
                status_running = False
                status_figth = True
                status_bottom = False
                status_fish = True
                custom_sleep(1)
                pydirectinput.press('0')
            else:
                pydirectinput.keyDown('alt')
                pydirectinput.press('r')
                pydirectinput.keyUp('alt')
                status_running = False
                status_figth = True
                status_bottom = False
                status_fish = True
                custom_sleep(1)
                pydirectinput.press('0')
            print(f"Simbol ditemukan dengan confidence {max_val:.2f}")
            
        elif max_val_font >= threshold and not status_bottom:
            tm.sleep(0.2)
            print("tulisan ditemukan")
            pyautogui.mouseDown(button="left")
            # tm.sleep(1)
            pyautogui.mouseUp(button="left")
            tm.sleep(1)
            pydirectinput.keyDown('alt')
            pydirectinput.press('t')
            pydirectinput.keyUp('alt')
            status_bottom = True    
            status_running = True     
            print(f"tulisan ditemukan dengan confidence {max_val_font:.2f}")   
        else:
            tm.sleep(0.2)
            continue

def finish():
    print("finish")
    pydirectinput.keyDown('alt')
    pydirectinput.press('r')
    pydirectinput.press('=')
    pydirectinput.keyUp('alt')
    pydirectinput.press('space')
    pyautogui.mouseDown(button="right")
    tm.sleep(2.9)
    pyautogui.mouseUp(button="right")
    tm.sleep(0.9)
    pydirectinput.press('space')
    pyautogui.mouseDown(button="left")
    pyautogui.mouseUp(button="left")
    tm.sleep(1.8)
    pydirectinput.press('x')
    # pydirectinput.press('x')
    pydirectinput.keyDown('alt')
    pydirectinput.press('-')
    pydirectinput.keyUp('alt')
    
    
    

# keyboard.add_hotkey('alt+t', toggle)
# keyboard.add_hotkey('alt+z', start)
# keyboard.add_hotkey('x', figth)
# keyboard.add_hotkey('0', start_rad_engine)
# keyboard.add_hotkey('9', finish)
def OnKeyboardEvent(event):
    # Deteksi Alt+Z
    if event.Key == 'Z' and event.Alt:
        start()
    
    # Deteksi X
    elif event.Key == 'X':
        fight()
    
    # Deteksi 9
    elif event.Key == '9':
        tm.sleep(0.5)
        finish()
    
    # Hotkey tambahan untuk keluar (Alt+Q)
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

# hook_thread_read = threading.Thread(target=engine_read)
# hook_thread_read.daemon = True  # Thread akan berhenti saat program utama berhenti
# hook_thread_read.start()


# keyboard.add_hotkey('s', create_tracker_screen)
print("engine starto detection")

while True:
    detection_symbol()
    # read_number()
    # create_tracker_screen()
    tm.sleep(0.2)
# Konversi screenshot ke format OpenCV (BGR)

