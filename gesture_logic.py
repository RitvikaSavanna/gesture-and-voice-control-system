import time

activation_time = 1.5
command_window = 3
s_command_window=0.5
buffer_time = 1
s_activation_time=2
activated = False
fist_start_time = None
last_command_time = 0
cooldown_start = 0

palm_start_time= None
p_activated=False

swipe_threshold = 0.12
history_length = 12
movement_smoothing = 3

s_history_length = 10

scroll_threshold = 0.09

position_history = []
s_position_history = []

gesture_buffer = []
buffer_size = 6


def classify_gesture(finger_state):

    if finger_state == [0,0,0,0,0]:
        return "FIST"

    elif finger_state == [0,1,1,0,0]:
        return "TWO"

    elif finger_state == [1,0,0,0,0]:
        return "THUMBS UP"
    elif finger_state == [1,1,1,1,1]:
        return "PALM"

    else:
        return "UNKNOWN"


def detect_finger_state(landmarks):

    finger_state = []

    if landmarks[4].x < landmarks[2].x:
        finger_state.append(1)
    else:
        finger_state.append(0)

    finger_tips = [8,12,16,20]
    finger_pips = [6,10,14,18]

    for tip,pip in zip(finger_tips,finger_pips):

        if landmarks[tip].y < landmarks[pip].y:
            finger_state.append(1)
        else:
            finger_state.append(0)

    return finger_state


def process_gesture(landmarks):

    global activated
    global p_activated
    global fist_start_time
    global palm_start_time
    global last_command_time
    global cooldown_start
    global position_history
    global gesture_buffer

    finger_state = detect_finger_state(landmarks)
    basic_gesture = classify_gesture(finger_state)

    index_tip = landmarks[8]
    current_x = index_tip.x
    current_y = index_tip.y

    confirmed_gesture = "Locked"

    if basic_gesture == "FIST":

        if fist_start_time is None:
            fist_start_time = time.time()

        if time.time() - fist_start_time >= activation_time and not p_activated:
            activated = True
            last_command_time = time.time()

    else:
        fist_start_time = None

    if basic_gesture == "PALM":

        if palm_start_time is None:
            palm_start_time = time.time()

        if time.time() - palm_start_time >= s_activation_time and not activated:
            p_activated = True
            last_command_time = time.time()

    else:
        palm_start_time = None

    gesture_buffer.append(basic_gesture)

    if len(gesture_buffer) > buffer_size:
        gesture_buffer.pop(0)

    stable_gesture = max(set(gesture_buffer), key=gesture_buffer.count)

    if activated and time.time() - cooldown_start >= buffer_time:

        position_history.append(current_x)

        if len(position_history) > history_length:
            position_history.pop(0)

        if len(position_history) == history_length:

            movement = position_history[-1] - position_history[0]

            if abs(movement) > swipe_threshold:

                if movement > 0:
                    confirmed_gesture = "SWIPE_RIGHT"
                else:
                    confirmed_gesture = "SWIPE_LEFT"

                last_command_time = time.time()
                cooldown_start = time.time()
                position_history.clear()

            else:

                if stable_gesture not in ["FIST","UNKNOWN"]:
                    confirmed_gesture = stable_gesture
                    last_command_time = time.time()
                    cooldown_start = time.time()
    elif p_activated:
        s_position_history.append(current_y)

        if len(s_position_history) > s_history_length:
            s_position_history.pop(0)

        if len(s_position_history) == s_history_length:

            p_movement = s_position_history[-1] - s_position_history[0]

            if abs(p_movement) > scroll_threshold:

                if p_movement > 0:
                    confirmed_gesture = "SCROLL_UP"
                else:
                    confirmed_gesture = "SCROLL_DOWN"

                last_command_time = time.time()
                position_history.clear()


    return confirmed_gesture, basic_gesture