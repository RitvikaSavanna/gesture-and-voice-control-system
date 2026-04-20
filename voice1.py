import speech_recognition as sr
import threading
import subprocess
import pyautogui
import pyperclip
import os
import time
import psutil

# ======================================================
# GLOBAL STATE
# ======================================================

running = True  
voice_active = False

open_time=None
voice_buffer=2


# ======================================================
# TEXT TO SPEECH
# ======================================================

def speak(text):
    """Speak text using Windows PowerShell"""

    def run():
        safe = text.replace("'", "")
        command = (
            f'powershell -WindowStyle Hidden -Command '
            f'"Add-Type -AssemblyName System.Speech;'
            f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{safe}\')"'
        )
        os.system(command)

    threading.Thread(target=run, daemon=True).start()


# ======================================================
# CLIPBOARD
# ======================================================

def read_clipboard():
    try:
        text = pyperclip.paste()

        if text:
            speak(text[:200])
        else:
            speak("Clipboard is empty")

    except:
        speak("Could not read clipboard")


# ======================================================
# COMMAND FUNCTIONS
# ======================================================

def open_youtube():
    speak("Opening YouTube")
    subprocess.Popen("start https://youtube.com", shell=True)

def open_chrome():
    speak("Opening Chrome")
    subprocess.Popen("start chrome", shell=True)
def open_ppt():
    speak("Opening PowerPoint")
    subprocess.Popen("start powerpnt", shell=True)

def open_explorer():
    speak("Opening file explorer")
    subprocess.Popen("explorer", shell=True)

def copy_text():
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.2)
    read_clipboard()

def paste_text():
    pyautogui.hotkey("ctrl", "v")
    speak("Pasted")

def read_selected():
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.2)
    read_clipboard()

def read_screen():
    speak("Reading screen")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.2)
    read_clipboard()

def tell_time():
    current = time.strftime("%I:%M %p")
    speak("The time is " + current)

def tell_date():
    today = time.strftime("%A %B %d")
    speak("Today is " + today)

def battery_status():
    battery = psutil.sensors_battery()
    speak(f"Battery is {battery.percent} percent")

def desktop():
    pyautogui.hotkey("win", "d")

def close_window():
    pyautogui.hotkey("alt", "f4")

def press_enter():
    pyautogui.press("enter")

def move_left():
    pyautogui.press("left")

def move_right():
    pyautogui.press("right")

def help_command():
    speak(
        "Commands available include open youtube, open chrome, scroll up, "
        "scroll down, copy, paste, read screen, battery status, time, date, "
        "search for something, go to desktop and close window."
    )


# ======================================================
# COMMAND MAP
# ======================================================

commands = {
    "open youtube": open_youtube,
    "open chrome": open_chrome,
    "open explorer": open_explorer,
    "open powerpoint": open_ppt,
    "open ppt":open_ppt,
    "copy": copy_text,
    "paste": paste_text,
    "read selected": read_selected,
    "read screen": read_screen,
    "time": tell_time,
    "date": tell_date,
    "battery": battery_status,
    "go to desktop": desktop,
    "close window": close_window,
    "press enter": press_enter,
    "move left": move_left,
    "move right": move_right,
    "help": help_command
}


# ======================================================
# VOICE LISTENER
# ======================================================

def voice_listener():

    global voice_active
    global running
    global open_time
    global voice_buffer

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8
    recognizer.energy_threshold = 2800
    recognizer.dynamic_energy_threshold = True

    mic = sr.Microphone()

    print("Say 'apple' to activate voice control")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while running:

        try:

            with mic as source:
                audio = recognizer.listen(
                    source,
                    timeout=4,
                    phrase_time_limit=4
                )

            text = recognizer.recognize_google(audio).lower().strip()

            print("Voice:", text)

            if text == "apple":
                #voice_active=True
                open_time=time.time()
                voice_active=not voice_active
                if voice_active:
                    speak("Voice activated")
                else:
                    speak("Voice deactivated")

                continue
            #print(time.time()-open_time)
            '''if voice_active and time.time()-open_time>=voice_buffer:
                    voice_active=False'''
                    
            if not voice_active:
                continue

            # SEARCH COMMAND
            if text.startswith("search for"):

                query = text.replace("search for", "").strip()

                speak("Searching for " + query)

                subprocess.Popen(
                    f"start https://www.google.com/search?q={query}",
                    shell=True
                )

                continue

            # EXECUTE COMMAND
            for command in commands:

                if command in text:
                    commands[command]()
                    break

        except sr.WaitTimeoutError:
            continue

        except sr.UnknownValueError:
            continue

        except Exception as e:
            print("Voice error:", e)


# ======================================================
# START VOICE SYSTEM
# ======================================================

def start_voice_system():

    voice_thread = threading.Thread(
        target=voice_listener,
        daemon=True
    )

    voice_thread.start()


# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    speak("Voice assistant ready. Say apple to activate.")

    start_voice_system()

    while True:
        time.sleep(1)

