import os
os.add_dll_directory(r"C:/Program Files/VideoLAN/VLC")

import cv2
import mediapipe as mp
import vlc
import time

# --- VLC Setup ---
media_folder = "media"
files = [os.path.join(media_folder, f) for f in os.listdir(media_folder)]
instance = vlc.Instance()
list_player = instance.media_list_player_new()
media_list = instance.media_list_new(files)
list_player.set_media_list(media_list)
player = list_player.get_media_player()

# Start VLC paused
list_player.play()
time.sleep(0.5)
player.pause()

# --- MediaPipe Hand Detector ---
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(min_detection_confidence=0.7,
                         min_tracking_confidence=0.7)

# Finger tip IDs
tip_ids = [4, 8, 12, 16, 20]

def count_fingers(hand_landmarks):
    fingers = []
    # Thumb: compare x-coords
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    # Other fingers: tip_y < pip_y
    for id in range(1, 5):
        if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)

# --- Webcam & Loop Setup ---
cap = cv2.VideoCapture(0)
prev_action = None
action_delay = 1.0   # seconds cooldown
last_time = time.time()
prev_frame_time = 0
fps = 0

# Instruction texts
instructions = [
    "0 Fingers : Pause",
    "1 Finger  : Play",
    "2 Fingers: Next Track",
    "3 Fingers: Previous Track",
    "4 Fingers: Volume Down",
    "5 Fingers: Volume Up",
    "Press 'Q' to Quit"
]

while True:
    success, img = cap.read()
    if not success:
        break

    # FPS calculation
    curr_frame_time = time.time()
    fps = 1 / (curr_frame_time - prev_frame_time) if prev_frame_time else 0
    prev_frame_time = curr_frame_time

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    action = None
    if results.multi_hand_landmarks:
        lm = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, lm, mp_hands.HAND_CONNECTIONS)
        fingers_up = count_fingers(lm)

        if time.time() - last_time > action_delay:
            if fingers_up == 0:
                # Pause only if currently playing
                if player.is_playing():
                    player.pause()
                    action = "Paused"
            elif fingers_up == 1:
                # Play only if currently not playing
                if not player.is_playing():
                    player.play()
                    action = "Playing"
            elif fingers_up == 2:
                list_player.next();       action = "Next Track"
            elif fingers_up == 3:
                list_player.previous();   action = "Previous Track"
            elif fingers_up == 4:
                vol = max(player.audio_get_volume() - 10, 0)
                player.audio_set_volume(vol)
                action = f"Volume Down: {vol}%"
            elif fingers_up == 5:
                vol = min(player.audio_get_volume() + 10, 100)
                player.audio_set_volume(vol)
                action = f"Volume Up: {vol}%"

            if action and action != prev_action:
                prev_action = action
                last_time = time.time()

    # Draw UI panel
    cv2.rectangle(img, (0, 0), (300, 180), (30, 30, 30), -1)
    for i, text in enumerate(instructions):
        cv2.putText(img, text, (10, 25 + i*25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # Display current action, volume, FPS
    if prev_action:
        cv2.putText(img, f"Action: {prev_action}", (10, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    vol = player.audio_get_volume()
    cv2.putText(img, f"Volume: {vol}%", (10, 280),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(img, f"FPS: {int(fps)}", (10, 320),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # Show result
    cv2.imshow("🎵 Hand Gesture VLC Control", img)

    # Exit on 'q' or window close
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
