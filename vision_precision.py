import pyautogui
import time
import math

mouse_on = False
m_fist_start_time = None
m_activation_time = 1.5

pyautogui.FAILSAFE=False

screen_width, screen_height = pyautogui.size()

frame_margin = 100

prev_mouse_x = 0
prev_mouse_y = 0
smoothening = 6

pinch_buffer = []
pinch_buffer_size = 4
pinch_threshold = 0.05


def toggle_mouse(gesture):

    global mouse_on
    global m_fist_start_time

    if gesture == "TWO":

        if m_fist_start_time is None:
            m_fist_start_time = time.time()

        if time.time() - m_fist_start_time >= m_activation_time:

            mouse_on = not mouse_on
            m_fist_start_time = None

    else:
        m_fist_start_time = None

    return mouse_on


def control_mouse(index_tip, thumb_tip, frame_w, frame_h):

    global prev_mouse_x, prev_mouse_y
    global pinch_buffer

    x = int(index_tip.x * frame_w)
    y = int(index_tip.y * frame_h)

    x = max(frame_margin, min(frame_w - frame_margin, x))
    y = max(frame_margin, min(frame_h - frame_margin, y))

    mouse_x = (x - frame_margin) * screen_width / (frame_w - 2 * frame_margin)
    mouse_y = (y - frame_margin) * screen_height / (frame_h - 2 * frame_margin)

    curr_x = prev_mouse_x + (mouse_x - prev_mouse_x) / smoothening
    curr_y = prev_mouse_y + (mouse_y - prev_mouse_y) / smoothening

    pyautogui.moveTo(int(curr_x), int(curr_y), duration=0)

    prev_mouse_x = curr_x
    prev_mouse_y = curr_y

    pinch_distance = math.sqrt(
        (thumb_tip.x-index_tip.x)**2 +
        (thumb_tip.y-index_tip.y)**2
    )

    pinch_buffer.append(pinch_distance)

    if len(pinch_buffer) > pinch_buffer_size:
        pinch_buffer.pop(0)

    avg_distance = sum(pinch_buffer) / len(pinch_buffer)

    if avg_distance < pinch_threshold:
        pyautogui.click()
        time.sleep(0.25)


def execute_command(gesture):

    if gesture == "SWIPE_RIGHT":
        pyautogui.press("left")

    elif gesture == "SWIPE_LEFT":
        pyautogui.press("right")

    elif gesture == "SCROLL_UP":
        pyautogui.press("up")
        
    elif gesture == "SCROLL_DOWN":
        pyautogui.press("down")

    elif gesture == "THUMBS UP":
        pyautogui.press("esc")