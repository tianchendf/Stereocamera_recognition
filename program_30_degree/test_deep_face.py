from deepface import DeepFace
import cv2

cap_path = 0 #"C:/Users/ZHT2SBY/Desktop/camera_recorrect-main/camera_recorrect-main_picture/anime6.mp4"
cap = cv2.VideoCapture(cap_path)
succuss = True
while succuss:
    succuss, img = cap.read()
    cv2.imwrite("C:/Users/ZHT2SBY/Desktop/camera_recorrect-main/program_30_degree/test.png", img)
    objs = DeepFace.analyze(img_path = "C:/Users/ZHT2SBY/Desktop/camera_recorrect-main/program_30_degree/test.png", 
            actions = ['age', 'gender'],
            detector_backend="mediapipe",
            enforce_detection = False
    )
    print(objs)
    cv2.imshow("test",img)
    cv2.waitKey(10)