import cv2
import mediapipe as mp
import numpy as np
import os
import sys
import time
from datetime import datetime


# =========================================================
# COLOR
# =========================================================

selected_hex = sys.argv[1] if len(sys.argv) > 1 else "#F6BFD7"


def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (b, g, r)


DRAW_COLOR = hex_to_bgr(selected_hex)


# =========================================================
# SETTINGS
# =========================================================

BRUSH_SIZE = 8
SAVE_COOLDOWN = 2.5
CLEAR_COOLDOWN = 1.5

os.makedirs("output", exist_ok=True)


# =========================================================
# MEDIAPIPE
# =========================================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)


# =========================================================
# CAMERA
# =========================================================

print("Starting Air Doodle camera...")

cap = cv2.VideoCapture(1, cv2.CAP_MSMF)

if not cap.isOpened():
    print("ERROR: Front camera did not open.")
    raise SystemExit

print("Front camera opened successfully.")


success, frame = cap.read()

if not success:
    print("ERROR: Could not read camera frame.")
    cap.release()
    raise SystemExit

frame = cv2.flip(frame, 1)

height, width, _ = frame.shape


# =========================================================
# CANVAS
# =========================================================

canvas = np.zeros_like(frame)

previous_point = None

last_save_time = 0
last_clear_time = 0

saved_message_until = 0
clear_message_until = 0


# =========================================================
# GESTURE FUNCTIONS
# =========================================================

def finger_is_up(landmarks, tip_id, pip_id):
    return landmarks[tip_id].y < landmarks[pip_id].y


def get_fingers(landmarks):
    return {
        "index": finger_is_up(landmarks, 8, 6),
        "middle": finger_is_up(landmarks, 12, 10),
        "ring": finger_is_up(landmarks, 16, 14),
        "pinky": finger_is_up(landmarks, 20, 18),
    }


def is_index_only(fingers):
    return (
        fingers["index"]
        and not fingers["middle"]
        and not fingers["ring"]
        and not fingers["pinky"]
    )


def is_two_fingers(fingers):
    return (
        fingers["index"]
        and fingers["middle"]
        and not fingers["ring"]
        and not fingers["pinky"]
    )


def is_open_palm(fingers):
    return (
        fingers["index"]
        and fingers["middle"]
        and fingers["ring"]
        and fingers["pinky"]
    )


def is_thumbs_up(landmarks, fingers):
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]

    thumb_up = thumb_tip.y < thumb_ip.y

    other_fingers_down = (
        not fingers["index"]
        and not fingers["middle"]
        and not fingers["ring"]
        and not fingers["pinky"]
    )

    return thumb_up and other_fingers_down


# =========================================================
# CANVAS COMBINE
# =========================================================

def merge_canvas(frame, canvas):
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(
        gray,
        1,
        255,
        cv2.THRESH_BINARY,
    )

    inverse = cv2.bitwise_not(mask)

    background = cv2.bitwise_and(
        frame,
        frame,
        mask=inverse,
    )

    drawing = cv2.bitwise_and(
        canvas,
        canvas,
        mask=mask,
    )

    return cv2.add(background, drawing)


# =========================================================
# MAIN LOOP
# =========================================================

while True:
    success, frame = cap.read()

    if not success:
        print("ERROR: Could not read camera frame.")
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB,
    )

    results = hands.process(rgb)

    mode = "Show your hand"


    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        landmarks = hand.landmark

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS,
        )

        fingers = get_fingers(landmarks)

        index_tip = landmarks[8]

        x = int(index_tip.x * width)
        y = int(index_tip.y * height)


        # -----------------------------------------
        # THUMBS UP = SAVE
        # -----------------------------------------

        if is_thumbs_up(landmarks, fingers):
            mode = "Saving photo"

            previous_point = None

            now = time.time()

            if now - last_save_time > SAVE_COOLDOWN:
                final_image = merge_canvas(
                    frame,
                    canvas,
                )

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                filename = (
                    f"output/"
                    f"air_doodle_{timestamp}.png"
                )

                cv2.imwrite(
                    filename,
                    final_image,
                )

                print(f"Saved: {filename}")

                last_save_time = now
                saved_message_until = now + 1.5


        # -----------------------------------------
        # OPEN PALM = CLEAR
        # -----------------------------------------

        elif is_open_palm(fingers):
            mode = "Clear canvas"

            previous_point = None

            now = time.time()

            if now - last_clear_time > CLEAR_COOLDOWN:
                canvas[:] = 0

                last_clear_time = now
                clear_message_until = now + 1.2


        # -----------------------------------------
        # TWO FINGERS = PAUSE
        # -----------------------------------------

        elif is_two_fingers(fingers):
            mode = "Paused"

            previous_point = None


        # -----------------------------------------
        # INDEX ONLY = DRAW
        # -----------------------------------------

        elif is_index_only(fingers):
            mode = "Drawing"

            cv2.circle(
                frame,
                (x, y),
                10,
                DRAW_COLOR,
                -1,
            )

            if previous_point is not None:
                cv2.line(
                    canvas,
                    previous_point,
                    (x, y),
                    DRAW_COLOR,
                    BRUSH_SIZE,
                    cv2.LINE_AA,
                )

            previous_point = (x, y)


        else:
            mode = "Hand detected"
            previous_point = None

    else:
        previous_point = None


    # =====================================================
    # MERGE DRAWING
    # =====================================================

    display = merge_canvas(
        frame,
        canvas,
    )


    # =====================================================
    # UI TEXT
    # =====================================================

    cv2.rectangle(
        display,
        (20, 20),
        (320, 75),
        (255, 250, 245),
        -1,
    )

    cv2.rectangle(
        display,
        (20, 20),
        (320, 75),
        (67, 55, 70),
        2,
    )

    cv2.circle(
        display,
        (48, 47),
        12,
        DRAW_COLOR,
        -1,
    )

    cv2.putText(
        display,
        mode,
        (72, 56),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (67, 55, 70),
        2,
        cv2.LINE_AA,
    )


    # Instructions
    instructions = [
        "Index finger = Draw",
        "Two fingers = Pause",
        "Open palm = Clear",
        "Thumbs up = Save",
        "Q = Quit",
    ]

    start_y = height - 145

    for i, text in enumerate(instructions):
        cv2.putText(
            display,
            text,
            (25, start_y + i * 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )


    # Save message
    if time.time() < saved_message_until:
        cv2.putText(
            display,
            "Photo saved!",
            (width - 220, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (80, 220, 120),
            2,
            cv2.LINE_AA,
        )


    # Clear message
    if time.time() < clear_message_until:
        cv2.putText(
            display,
            "Canvas cleared!",
            (width - 260, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (210, 140, 220),
            2,
            cv2.LINE_AA,
        )


    cv2.imshow(
        "Air Doodle",
        display,
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =========================================================
# CLEANUP
# =========================================================

cap.release()
hands.close()
cv2.destroyAllWindows()

print("Air Doodle closed.")