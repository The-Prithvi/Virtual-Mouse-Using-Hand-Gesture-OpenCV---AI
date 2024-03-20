import cv2
import mediapipe as mp
import pyautogui
import screen_brightness_control as sbc

drawing_utils = mp.solutions.drawing_utils
capture = cv2.VideoCapture(0)
palmDetect = mp.solutions.hands.Hands()
screen_width, screen_height = pyautogui.size()

index_y = 0    #initially
thumb_y = 0    #initially
ring_y = 0    #initially
middle_y = 0    #initially

while True:
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    output = palmDetect.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    hands = output.multi_hand_landmarks
    # print(hands)
    pyautogui.FAILSAFE = False
    if hands:
        for i in hands:
            drawing_utils.draw_landmarks(frame, i)  #draws landmark over palm
            for id, axisValue in enumerate(i.landmark):
                x = int(axisValue.x * frame_width)
                y = int(axisValue.y * frame_height) 
                # print(x, y)
                
                # if id == 20:          # pinky
                #     cv2.circle(img = frame, center=(x,y), radius = 15 , color=(0, 100, 255))
                #     pinky_x = screen_width / frame_width * x
                #     pinky_y = screen_height / frame_height * y
                    
                if id == 16:          # ring
                    cv2.circle(img = frame, center=(x,y), radius = 15 , color=(0, 100, 255))
                    ring_x = screen_width / (frame_width) * x
                    ring_y = screen_height / (frame_height) * y
                
                if id == 4:          # thumb
                    cv2.circle(img = frame, center=(x,y), radius = 15 , color=(0, 100, 255))
                    thumb_x = (screen_width / frame_width * x) + 150
                    thumb_y = (screen_height/ frame_height * y) + 50
                    # print(int(abs(index_x/10)), end = "   ")
                    # print(int(abs(index_y/10)))
                    pyautogui.moveTo(thumb_x ,thumb_y, duration=-1)
                
                if id == 8:          # index
                    cv2.circle(img = frame, center=(x,y), radius = 15 , color=(0, 100, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    # print(int(abs(index_x/10)), end = "   ")
                    # print(int(abs(index_y/10)))
                    
                # previous_ring_y = ring_y
                   
                if id == 12:         # middle
                    cv2.circle(img = frame, center=(x,y), radius = 15 , color=(0, 100, 255))
                    middle_y = screen_height / frame_height * y
                    # print((middle_y - thumb_y))
                    # print((index_y - thumb_y), end = "   ")
                    # print((middle_y - thumb_y))
                    # print(thumb_y - ring_y)
                    # print(ring_y)
                    
                    if thumb_y - ring_y <= 80:
                        print("brightness change")
                        # print(thumb_x/10)
                        thx = thumb_x/10
                        if thx < 40:
                            sbc.set_brightness(0)
                        elif thx > 40 and thx < 60:
                            sbc.set_brightness(15)
                        elif thx > 60 and thx < 80:
                            sbc.set_brightness(30)
                        elif thx > 80 and thx < 100:
                            sbc.set_brightness(40)
                        elif thx > 100 and thx < 120:
                            sbc.set_brightness(50)
                        elif thx > 120 and thx < 140:
                            sbc.set_brightness(60)
                        elif thx > 160 and thx < 180:
                            sbc.set_brightness(75)
                        elif thx > 180 and thx < 200:
                            sbc.set_brightness(85)
                        elif thx > 200:
                            sbc.set_brightness(100)
                        
                        
                        pyautogui.sleep(1)
                        
                    if index_y - thumb_y >= -115:
                        pyautogui.click(button='left')
                        print("LEFT CLICK")
                        # pyautogui.sleep(1)
                        
                    if index_y - middle_y <= -100:
                        pyautogui.click(button='right')
                        print("RIGHT CLICK")
                        pyautogui.sleep(1)
                
            
    cv2.imshow('v_mouse', frame)
    cv2.waitKey(1)