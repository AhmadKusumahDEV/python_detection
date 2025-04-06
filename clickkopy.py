import pyautogui as pg
import time as tm
import random
import pyWinhook as ph
import pythoncom
import threading
import keyboard

running = False  # Toggle state
wild = False

def making_tea() :
    """Perform the make tea automation"""
    global running

    while running:
        if not running:
            return
        pg.mouseDown(button="left")
        pg.mouseUp(button="left")
        tm.sleep(0.1)
        pg.press("space")
        pg.mouseDown(button="left")
        pg.mouseUp(button="left")

def custom_sleep(duriton): 
    global running
    global wild
    if running:
        for z in range(duriton):
            if not running:
                return
            tm.sleep(1)
    elif wild:
        for z in range(duriton):
            if not wild:
                return
            tm.sleep(1)
        
def custom_sleep_special(duriton):
    global running
    interval = 0.1
    lop = duriton / interval
    for _ in range(lop):
        if not running:
            return
        tm.sleep(interval)

def toggle():
    """Toggle the automation on/off when pressing 'p'"""
    global running
    running = not running
    print(f"Automation {'started' if running else 'stopped'}")
    
def togglewild():
    """Togglewild the automation on/off when pressing 'p'"""
    global wild
    wild = not wild
    print(f"Automation wild {'started' if wild else 'stopped'}")

def automation_cast(a=5,b=4, c=1):
    """Simulate a fishing cast action"""
    print(a,b)
    pg.mouseDown(button="left")
    tm.sleep(a)
    pg.mouseUp(button="left")
    tm.sleep(b)
    if c == 1:
        pg.press("y")
    return
    
def automation_casting():
    """Perform the cast simulater automation"""
    global running

    while running:
        casts = 10  # Adjust as needed

        for j in range(casts):
            automation_cast(5,48,2)
            print("do casting : ", j)
            pg.mouseDown(button="left")
            if not running:
                return
            tm.sleep(70)
            if not running:
                return
            pg.mouseUp(button="left")
            tm.sleep(3)
            if not running:
                return
            print("done")
            if not running:
                return
            


def automation_jig_step():
    """Perform the jigging step automation"""
    global running
    if not running:
        return
    while running:
        casts = 5  # Adjust as needed
        clicks = 50  # Adjust as needed
        change_lure = 2  # 1 = Yes, 2 = No

        for j in range(casts):
            for i in range(clicks):
                if not running:
                    return  # Stop immediately if toggled off
               
                random_sleep_time = random.uniform(0.7, 1.0)

                if i + 1 == clicks:
                    pg.mouseDown(button="left")
                    custom_sleep(25)
                    pg.mouseUp(button="left")
                    # pg.press("y")
                    tm.sleep(1)

                    if change_lure == 1 and j + 1 == casts:
                        print("Finished")
                        return

                    automation_cast(3,4,2)
                    print("Execute automation cast")
                    tm.sleep(7)
                    print("Waiting for bottom lure")
                    break
                else: 
                    # tm.sleep(3.5) ## default
                    # pernah custom 1.8
                    tm.sleep(3.5) ## custom
                    pg.mouseDown(button="left")
                    tm.sleep(random_sleep_time)
                    pg.mouseUp(button="left")
                    print(f"Click {i + 1}")


def Pirking():
    """Perform the auto pirking automation"""
    global running
    if not running:
        return
    while running:
        try:
        # Kode utama Anda
            pg.mouseDown(button="Right")
            tm.sleep(0.3)
        finally:
        # Cleanup ketika program berhenti
            pg.mouseUp(button="Right")
            print("Mouse released successfully!")
        if not running:
            return
        custom_sleep(3)
        
def Strong_Pirking():
    """Perform the auto pirking automation"""
    global running
    if not running:
        return
    while running:
        pg.mouseDown(button="Right")
        if not running:
            return
        tm.sleep(0.6)
        pg.mouseUp(button="Right")
        if not running:
            return
        custom_sleep(3)
        if not running:
            return

def auto_wild():
    while wild:
        keyboard.press("shift")
        pg.mouseDown(button="left")
        custom_sleep(50)
        pg.mouseUp(button="left")
        keyboard.release("shift")

def OnKeyboardEvent(event):
    # Deteksi Alt+T
    if event.Key == 'T' and event.Alt:  # 'T' adalah karakter yang ditekan
        toggle()
    # Deteksi Alt+R
    elif event.Key == 'R' and event.Alt:
        togglewild()
    return True  # Return True agar event tetap diproses oleh aplikasi lain

def start_hook():
    hook_manager = ph.HookManager()
    hook_manager.KeyDown = OnKeyboardEvent
    hook_manager.HookKeyboard()
    pythoncom.PumpMessages()

# Jalankan hook keyboard di thread terpisah
hook_thread = threading.Thread(target=start_hook)
hook_thread.daemon = True  # Thread akan berhenti saat program utama berhenti
hook_thread.start()
# keyboard.add_hotkey('/', automation_cast)
# keyboard.add_hotkey('alt+t', toggle)
# keyboard.add_hotkey('alt+r', togglewild)
# keyboard.add_hotkey('q', lambda: exit())  # Press 'q' to exit the script

print("Press 't' to start/stop the automation.")
print("Press 'q' to exit the script.")  

while True:
    # making_tea()
    Pirking()
    # Strong_Pirking()
    # automation_jig_step()
        # automation_casting()
    auto_wild()
    tm.sleep(0.1)  # Prevent CPU overload