# **PoseView**

## **Overview**
PoseView is a real-time **posture estimation and analysis system** that leverages computer vision to monitor user posture, identify bad habits, and provide instant feedback. The application includes an **alert system** that notifies users of bad posture through Telegram, promoting ergonomic awareness in workplaces, schools, or home settings.

---

## **Objectives**
- To monitor and analyze posture in real-time using a webcam.
- To identify bad posture habits and provide instant alerts through messaging platforms.
- To visualize posture landmarks and inclinations for better understanding and analysis.
- To help users maintain healthy posture habits and avoid long-term ergonomic issues.

---

## **Features**
### **Real-Time Posture Detection**:
- Utilizes **MediaPipe Pose** to identify and track key body landmarks (e.g., shoulders, hips, ears).
- Calculates neck and torso inclinations to assess posture quality.

### **Alert Messaging System**:
- Sends **Telegram alerts** using the **Telebot API** if bad posture persists for more than 20 seconds.
- Encourages users to correct their posture immediately.

### **Interactive Visual Feedback**:
- Displays posture landmarks and inclination angles in real-time for user analysis.
- Categorizes posture as:
  - **Good Posture**: Displayed with green text.
  - **Bad Posture**: Displayed with red text and triggers alerts.

### **Customizable Thresholds**:
- Adjustable neck and torso inclination thresholds for personalized posture monitoring.

### **Responsive Error Handling**:
- Ensures smooth operation by gracefully handling invalid frames, input errors, or API failures.

### **User Calibration**:
- Supports calibration of good posture baselines to enhance detection accuracy.

---

## **Technologies Used**
### **Core Frameworks**:
- **OpenCV**: For webcam input and real-time video processing.
- **MediaPipe Pose**: For body landmark detection and tracking.

### **Programming**:
- **Python**: The primary language for the application.

### **Alerting System**:
- **Telebot API**: For sending real-time alerts via Telegram.

---

## **Getting Started**
### **Prerequisites**:
- Python 3.7+ installed on your machine.
- Access to a webcam.
- A Telegram bot with its token and chat ID configured.

---

## **Installation**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/PoseView.git
   cd PoseView
  
2. **Install Dependencies: Ensure the required Python libraries are installed**:
  ```bash
  pip install opencv-python mediapipe requests

3. **Configure Telegram Bot**:
  Open the pose_view.py file.
  Replace placeholders in these lines with your bot's credentials:

  ```python
  bot_token = "Enter Token of Telegram bot"
  chat_id = "Enter ChatID of telegram"

4. **Run the Application**:
  ```bash
  python pose_view.py
