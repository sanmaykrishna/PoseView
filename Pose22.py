import cv2
import math as m
import mediapipe as mp
import time
import requests # For sending Telegram messages
import telebot

# Define Telegram bot information (replace with yours)
bot_token = "Enter Token of Telegram bot"
chat_id = "Enter ChatID of telegram"

# Calculate distance
def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

# Calculate angle
def findAngle(x1, y1, x2, y2):
    if y1 == 0 or y2 == 0:
        # Handle the case: return a default value (e.g., 0) or raise an exception
        return 0  # Replace with appropriate action
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

# Initialize mediapipe pose class
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

bad_posture_start_time=None
alerted=False 
alert_duration =20

# Send Telegram message
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=payload)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)  # Webcam input

    # Font type
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Track bad posture duration
    bad_posture_start = None
    alert_duration = 20
    alerted = False
    
# Calibration posture (adjust based on your preference)
    calibration_posture_x = 0  # Set X-coordinate of a reference point in good posture (optional)
    calibration_posture_y = 0  # Set Y-coordinate of a reference point in good posture (optional)

    while cap.isOpened():
        # Capture frames
        success, image = cap.read()
        if not success:
            print("Null Frames")
            break

        # Get height and width
        h, w = image.shape[:2]

        # Convert the BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image
        keypoints = pose.process(image)

        # Convert the image back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Use lm and lmPose as representative of the following methods
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark

        # Acquire landmark coordinates
        if lm is not None:
             # Draw lines to connect landmarks
            connections = mp_pose.POSE_CONNECTIONS
            for connection in connections:
                landmark_from = connection[0]
                landmark_to = connection[1]
                x0, y0 = int(lm.landmark[landmark_from].x * w), int(lm.landmark[landmark_from].y * h)
                x1, y1 = int(lm.landmark[landmark_to].x * w), int(lm.landmark[landmark_to].y * h)
                cv2.line(image, (x0, y0), (x1, y1), (255, 0, 0), 2)

            # Analyze posture (including right side)
            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
            l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
            l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
            l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

            r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
            r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
            r_ear_x = int(lm.landmark[lmPose.RIGHT_EAR].x * w)
            r_ear_y = int(lm.landmark[lmPose.RIGHT_EAR].y * h)
            r_hip_x = int(lm.landmark[lmPose.RIGHT_HIP].x * w)
            r_hip_y = int(lm.landmark[lmPose.RIGHT_HIP].y * h)

            neck_inclination_left = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            neck_inclination_right = findAngle(r_shldr_x, r_shldr_y, r_ear_x, r_ear_y)
            torso_inclination_left = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)
            torso_inclination_right = findAngle(r_hip_x, r_hip_y, r_shldr_x, r_shldr_y)

            # Improved posture assessment (considering thresholds)
            posture_text = "Good Posture"
            text_color = (0, 255, 0)  # Green for good posture

            # Adjust thresholds based on your observations and preferences
            neck_threshold = 30  # Lower threshold for neck inclination
            torso_threshold = 15  # Lower threshold for torso inclination
            rounding_threshold = 0.3  # Higher threshold for forward rounding (adjust as needed)

            if neck_inclination_left > neck_threshold or neck_inclination_right > neck_threshold or torso_inclination_left > torso_threshold or torso_inclination_right > torso_threshold:
                posture_text = "Bad Posture"
                text_color = (0, 0, 255)  # Red for bad posture

                if not alerted:
                    bad_posture_start_time = time.time()  # Start timer for bad posture
                    alerted = True
                                        
                else:
                    if time.time() - bad_posture_start_time > alert_duration:
                        # Send alert message
                        print("Sending alert message...")
                        send_telegram_alert("Bad posture detected for more than 20 secs correct it!!!!")  # Send Telegram alert
                        print("alert sended")
                        alerted = False  # Reset alert flag
                        bad_posture_start_time = None  # Reset the timer.

            else:
                if alerted:
                    alerted = False
             # Optional: Calibration for good posture baseline (adjust if needed)
            if calibration_posture_x != 0 and calibration_posture_y != 0:
                ref_x_offset = calibration_posture_x - spine_mid_x
                ref_y_offset = calibration_posture_y - spine_mid_y
                spine_mid_x += ref_x_offset
                spine_mid_y += ref_y_offset
            # Draw landmarks with different colors
            for landmark in lm.landmark:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                if landmark in [lmPose.LEFT_SHOULDER, lmPose.LEFT_EAR, lmPose.LEFT_HIP, lmPose.RIGHT_SHOULDER, lmPose.RIGHT_EAR, lmPose.RIGHT_HIP]:
                    cv2.circle(image, (x, y), 5, (255, 0, 255), -1)
                else:
                    cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

            # Put text: Posture and angles (white color)
            angle_text_string = 'Neck (L/R): ' + str(int(neck_inclination_left)) + '/' + str(int(neck_inclination_right)) + '  Torso (L/R): ' + str(int(torso_inclination_left)) + '/' + str(int(torso_inclination_right))
            cv2.putText(image, posture_text, (10, 30), font, 0.9, text_color, 2, cv2.LINE_AA)
            cv2.putText(image, angle_text_string, (10, 60), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)  # White for angles

        # Display in full screen
        cv2.namedWindow('MediaPipe Pose', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('MediaPipe Pose', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        cv2.resizeWindow('MediaPipe Pose', 640, 480)  
        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
