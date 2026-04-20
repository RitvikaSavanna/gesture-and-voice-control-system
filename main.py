import cv2
import mediapipe as mp
import time

import gesture_logic
from gesture_logic import process_gesture
from vision_precision import toggle_mouse, control_mouse, execute_command
import voice_module
from voice_module import start_voice_system, speak, voice_listener,read_clipboard
f2=0
f3=0
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

mouse_on=False
activated=False

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
start_voice_system()
confirmed_gesture = "Locked"

pTime = 0

while True:
    
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame,1)

    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    frame_h, frame_w, _ = frame.shape

    if gesture_logic.activated and (time.time() - gesture_logic.last_command_time > gesture_logic.command_window):
        gesture_logic.activated = False
        confirmed_gesture = "Locked"
        speak("System Locked")
        f2=0
        gesture_logic.position_history.clear()
    if gesture_logic.p_activated and (time.time() - gesture_logic.last_command_time > gesture_logic.s_command_window):
        gesture_logic.p_activated = False
        gesture_logic.s_position_history.clear()
        f3=0
 
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            landmarks = hand_landmarks.landmark

            confirmed_gesture, basic_gesture = process_gesture(landmarks)
            previous_mouse_state = mouse_on
            mouse_on = toggle_mouse(basic_gesture)

            if mouse_on != previous_mouse_state:
                if mouse_on:
                    speak("Mouse on")
                else:
                    speak("Mouse off")

            index_tip = landmarks[8]
            thumb_tip = landmarks[4]

            if mouse_on:
                control_mouse(index_tip, thumb_tip, frame_w, frame_h)

            if confirmed_gesture!="Locked":
                execute_command(confirmed_gesture)
                if confirmed_gesture == "SWIPE_RIGHT":
                    speak("Right")

                elif confirmed_gesture == "SWIPE_LEFT":
                    speak("Left")

                elif confirmed_gesture == "THUMBS UP":
                    speak("Exiting")
                confirmed_gesture = "Locked"

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.putText(frame,f'Gesture: {confirmed_gesture}',
                (10,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)

    if gesture_logic.activated:
        if(f2==0):
            speak("System activated")
            f2=1
        cv2.putText(frame,"SYSTEM ACTIVE",
                    (10,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2)
    else:
        cv2.putText(frame,f"HOLD FIST {gesture_logic.activation_time}s TO ACTIVATE",
                    (10,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    2)

    if mouse_on:
        cv2.putText(frame,"MOUSE ON",
                    (10,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,0,0),
                    2)
    elif gesture_logic.p_activated:
        if(f3==0):
            speak("Scroll on")
            f3=1
        cv2.putText(frame,"SCROLL ON",
                    (10,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,0,0),
                    2)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(frame,f'FPS: {int(fps)}',
                (500,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,0),
                2)
    if not voice_module.voice_active:
        cv2.putText(frame,"Say 'apple' to activate the system",
                            (10,400),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255,0,0),
                            2)

    cv2.imshow("Hand Detection",frame)
    cv2.setWindowProperty("Hand Detection",cv2.WND_PROP_TOPMOST,1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()