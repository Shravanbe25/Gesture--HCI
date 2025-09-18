
import cv2
import numpy as np
try:
    import mediapipe as mp
except Exception:
    mp = None
try:
    import pyautogui
except Exception:
    pyautogui = None

# Gesture-Based HCI demo:
# - Tracks hand landmarks (if MediaPipe is installed).
# - Moves a virtual cursor (prints coords if pyautogui not available).
# - Detects a 'pinch' to simulate a click.

def move_cursor(x, y):
    if pyautogui is not None:
        try:
            pyautogui.moveTo(x, y)
        except Exception:
            print(f"[DEBUG] Move cursor to ({x}, {y})")
    else:
        print(f"[DEBUG] Cursor -> ({x}, {y})")

def click():
    if pyautogui is not None:
        try:
            pyautogui.click()
        except Exception:
            print("[DEBUG] Click")
    else:
        print("[DEBUG] Click")

def run_demo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam. Exiting demo.")
        return

    if mp is not None:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        mp_draw = mp.solutions.drawing_utils
    else:
        hands = None
        mp_draw = None

    screen_w, screen_h = (1920, 1080)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        if hands is not None:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)
            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:
                    # Index tip (8) and thumb tip (4)
                    index_tip = handLms.landmark[8]
                    thumb_tip = handLms.landmark[4]

                    cx = int(index_tip.x * w)
                    cy = int(index_tip.y * h)

                    # Map to pretend screen coords
                    sx = int(index_tip.x * screen_w)
                    sy = int(index_tip.y * screen_h)
                    move_cursor(sx, sy)

                    # Detect pinch
                    dx = (index_tip.x - thumb_tip.x) * w
                    dy = (index_tip.y - thumb_tip.y) * h
                    dist = (dx**2 + dy**2) ** 0.5
                    if dist < 30:
                        click()
                        cv2.putText(frame, "CLICK!", (cx, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

                    if mp_draw is not None:
                        mp_draw.draw_landmarks(frame, handLms, mp.solutions.hands.HAND_CONNECTIONS)

        cv2.putText(frame, "Gesture HCI Demo - Press 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.imshow("Gesture HCI", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_demo()
