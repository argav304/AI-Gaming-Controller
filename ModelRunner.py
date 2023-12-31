from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import tensorflow as tf
import pyautogui as pg
import mediapipe as mp
import numpy as np
import cv2


mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities
mp_pose = mp.solutions.pose  # Inbuilt poses
pose_connections = [(15, 16), (11, 12)]  # shoulder and wrist connection
actions = np.array(['null', 'apply-throttle', 'release-throttle'])  # the throttle control actions
colors = [(245, 117, 16), (117, 245, 16),
          (16, 117, 245)]  # colors to show the predicted values of the throttle controls
turn_controls = {'null': 0, 'left': 1, 'right': 2}  # values for the turn controls

# BUILDING THE MODEL
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 258)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.load_weights('./Models/actions.h5')
tf.keras.utils.disable_interactive_logging() # to stop logging of the model, to enable logging remove in ModelRunner method and in main.py



# DRAWING THE POSITION MARKERS AND THE CONNECTIONS
def draw_styled_landmarks(image, results):
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, pose_connections,
                              mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                              )


# Draw landmarks stylized
def draw_styled_landmarks_all(image, results):
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                              )
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                              )
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                              )


# FOR THE TURN CONTROL
def calculate_angle(a, b, c, d):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    d = np.array(d)
    radians = np.arctan2(d[1] - c[1], d[0] - c[0]) - np.arctan2(b[1] - a[1], b[0] - a[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if a[1] > b[
        1] and angle > 180.0:  # if left wrist above right and angle over 180.0(likely  around 300-360), convert to
        # under 0 to 180
        angle = 360.0 - angle
    if a[1] < b[1] and angle < 180:
        angle = 360.0 - angle
    return angle


# LANDMARK DETECTION
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writeable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writeable
    return image, results


# extracting the x,y co-ordinates of landmarks detected by mediapipe and storing in numpy arrays, here left and right
# hands with the posture
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in
                     results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
    left_hand = np.array([[res.x, res.y, res.z] for res in
                          results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(
        21 * 3)
    right_hand = np.array([[res.x, res.y, res.z] for res in
                           results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(
        21 * 3)
    return np.concatenate([pose, left_hand, right_hand])


# CONVERT ANGLE TO TURN CONTROL -> LEFT OR RIGHT OR NEUTRAL
def angle_to_turn(angle):
    if 17.0 < angle < 180.0:
        return turn_controls['left']
    elif 180.0 < angle < 343.0:
        return turn_controls['right']
    else:
        return turn_controls['null']


# CONVERTS INPUTS TO THROTTLE CONTROLS
def throttle_controller(throttle_input, accelarate):
    if throttle_input == 'apply-throttle':
        if accelarate:
            return
        else:
            pg.keyUp('down')
            pg.keyDown('up')
            return
    if throttle_input == 'release-throttle':
        if not accelarate:
            return
        else:
            pg.keyUp('up')
            pg.keyDown('down')
            return


# CONVERTS INPUTS TO ACTUAL KEY CLICKS
def turn_controller(turn, prev_turn):
    if turn == turn_controls['left']:
        if prev_turn == turn_controls['null']:
            pg.keyDown('left')
            return
        if prev_turn == turn_controls['right']:
            pg.keyUp('right')
            pg.keyDown('left')
            return
    if turn == turn_controls['right']:
        if prev_turn == turn_controls['null']:
            pg.keyDown('right')
            return
        if prev_turn == turn_controls['left']:
            pg.keyUp('left')
            pg.keyDown('right')
            return
    if turn == turn_controls['null']:
        if prev_turn == turn_controls['null']:
            return
        if prev_turn == turn_controls['left']:
            pg.keyUp('left')
            return
        if prev_turn == turn_controls['right']:
            pg.keyUp('right')
            return


# put action  prediction probabilities on the frame
def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
        cv2.putText(output_frame, '{} : {}'.format(actions[num], prob), (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2,
                    cv2.LINE_AA)

    return output_frame


def toggle_start_core_flag(value):
    global Start_Core_Flag
    Start_Core_Flag = value


def toggle_key_click_flag(value):
    global Key_Click_Flag
    Key_Click_Flag = value


# ---------------------------------------------------------------------------------------------------------------------





Start_Core_Flag = False  # This flag when set, allows for model prediction and key presses to occur,i.e. core
# functionality
Key_Click_Flag = False  # flag, if true allows for camera detections to trigger key clicks, else not


# MAIN APPLICATION METHOD
def ModelRunner(cap, run_event, frame_queue):
    tf.keras.utils.disable_interactive_logging() # to stop logging of the model
    global Start_Core_Flag, Key_Click_Flag
    # Set mediapipe model
    holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # array to append frames(30 for current model) to ship of to the model to make predictions and minimum predicted
    # prob of any action
    sequence = []
    threshold = 0.65
    # controls
    angle = 0.0
    accelerate = False
    turn = turn_controls['null']
    turn_controls_inv = {0: 'null', 1: 'left', 2: 'right'}  # key and value swapped
    # THE MAIN LOOP WHICH RUNS TO GET ACTIONS AND GIVE FINAL CONTROL PREDICTIONS
    while run_event.is_set():
        # Read feed
        ret, frame = cap.read()

        # Make detections
        image, results = mediapipe_detection(frame, holistic)
        # Draw landmarks
        draw_styled_landmarks(image, results)
        # 2. Prediction logic
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]

        if len(sequence) == 30 and Start_Core_Flag:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]

            # Visualize prediction probabilities
            image = prob_viz(res, actions, image, colors)

        try:
            landmarks = results.pose_landmarks.landmark
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            # Throttle controls
            if res[np.argmax(res)] > threshold and actions[
                np.argmax(res)] != 'null' and Key_Click_Flag and Start_Core_Flag:
                throttle_controller(actions[np.argmax(res)], accelerate)
            else:
                pass
            accelerate = True if actions[np.argmax(res)] == 'apply-throttle' else False
            if Start_Core_Flag:
                angle = calculate_angle(left_wrist, right_wrist, left_shoulder, right_shoulder)

        except AttributeError:
            pass
        except UnboundLocalError:
            pass

        # Turning
        prev_turn = turn
        turn = angle_to_turn(angle)
        if Key_Click_Flag and Start_Core_Flag:
            turn_controller(turn, prev_turn)
        try:
            cv2.putText(image, str(angle),
                        tuple(np.multiply(left_wrist, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )
        except UnboundLocalError:
            pass
        cv2.putText(image,
                    'Throttle: {} | turn: {} | keyclick: {}'.format(accelerate, turn_controls_inv[turn],
                                                                    Key_Click_Flag),
                    (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.632, (0, 255, 0), 4, cv2.LINE_AA
                    )

        # placing final processed image in the queue for GUI to pick up later when it can
        frame_queue.put(image)




