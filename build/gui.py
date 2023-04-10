


from pathlib import Path
import cv2
import mediapipe as mp
import pyautogui
import pydirectinput

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"Path of assets you have to give here")

def hand():

	cap = cv2.VideoCapture(0)
	hand_detector = mp.solutions.hands.Hands()
	drawing_utils = mp.solutions.drawing_utils
	screen_width, screen_height = pyautogui.size()
	index_y = 0
	while True:      
         _, frame = cap.read()
         frame = cv2.flip(frame, 1)
         frame_height, frame_width, _ = frame.shape
         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         output = hand_detector.process(rgb_frame)
         hands = output.multi_hand_landmarks
         if hands:
              for hand in hands:
                  drawing_utils.draw_landmarks(frame, hand)
                  landmarks = hand.landmark
                  for id, landmark in enumerate(landmarks):
                      x = int(landmark.x*frame_width)
                      y = int(landmark.y*frame_height)
                      if id == 8:
                          cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                          index_x = screen_width/frame_width*x
                          index_y = screen_height/frame_height*y
                          pyautogui.moveTo(index_x, index_y)
                        #   pydirectinput.moveTo(index_x, index_y)
                      if id == 4:
                          cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                          thumb_x = screen_width/frame_width*x
                          thumb_y = screen_height/frame_height*y
                          if abs(index_y - thumb_y) < 30:
                              pyautogui.click()
                            #   pydirectinput.click()
                              pyautogui.sleep(1)
                        #   elif abs(index_y - thumb_y) < 100:
                        #       pyautogui.moveTo(index_x, index_y)

                                                            
         cv2.imshow('Virtual Mouse', frame)
         cv2.waitKey(1)
         k = cv2.waitKey(1)
         if k ==ord('q'):
           cv2.destroyAllWindows()
           break


def eyes():
      cam = cv2.VideoCapture(0)
      face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
      screen_w, screen_h = pyautogui.size()
      while True:
            _, frame = cam.read()
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w, _ = frame.shape
            if landmark_points:
                landmarks = landmark_points[0].landmark
                for id, landmark in enumerate(landmarks[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0))
                    if id == 1:
                        screen_x = screen_w * landmark.x
                        screen_y = screen_h * landmark.y
                        pyautogui.moveTo(screen_x, screen_y)
                left = [landmarks[145], landmarks[159]]
                for landmark in left:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))
                if (left[0].y - left[1].y) < 0.004:
                    pyautogui.click()
                    pyautogui.sleep(1)
            cv2.imshow('Eye Controlled Mouse', frame)
            # cv2.waitKey(1)
            key = cv2.waitKey(1)
          
            if key == ord('q'):
             cv2.destroyAllWindows()
             break    


	  

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1411x772")
window.configure(bg = "#141614")


canvas = Canvas(
    window,
    bg = "#141614",
    height = 772,
    width = 1411,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    705.0,
    365.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=hand,
    relief="flat"
)
button_1.place(
    x=927.0,
    y=125.0,
    width=400.0,
    height=180.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=eyes,
    relief="flat"
)
button_2.place(
    x=937.0,
    y=386.0,
    width=390.0,
    height=176.0
)

canvas.create_text(
    781.0,
    660.0,
    anchor="nw",
    text="     For Escape Press “q” ",
    fill="#18FF74",
    font=("Inter SemiBold", 48 * -1)
)
window.resizable(False, False)
window.mainloop()
