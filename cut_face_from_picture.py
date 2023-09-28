import cv2
from PIL import Image
import math

class cut_face_from_picture():
    def __init__(self):
        self.raw_pictiure_path = "C:/Users/ZHT2SBY/Desktop/camera_recorrect-main/yolo/gape_picture_"
        self.location_data_PATH = "C:/Users/ZHT2SBY/Desktop/camera_recorrect-main/yolo/data_"
        self.result_PATH = "C:/Users/ZHT2SBY/Desktop/camera_recorrect-main/yolo/face_"
    def cut_picture(self,id):
        raw_pictiure_path = self.raw_pictiure_path + str(id) + ".png"
        location_data_PATH = self.location_data_PATH + str(id) + ".txt"
        self.txt_file = open(location_data_PATH,'r')
        result_PATH = self.result_PATH + str(id) + ".png"
        
        #https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
        #特征点的编号
        point_index = [0,2,5,7,8,9, 10]
        point_location = []
        self.txt_file.seek(0, 0)
        #x横向 y竖向
        for i in point_index:
            x = int(self.txt_file.readline())
            y = int(self.txt_file.readline())
            point_location.append([x,y])
        #w为横向的宽 h 为纵向的长
        #right_w = abs(point_location[0][0] - point_location[3][0]) + max(abs(point_location[0][0] - point_location[4][0])/2 , abs(point_location[0][0] - point_location[6][0])/2)
        #left_w = abs(point_location[0][0] - point_location[4][0]) + max(abs(point_location[0][0] - point_location[3][0])/2 , abs(point_location[0][0] - point_location[5][0])/2)
        #if (point_location[1][1] + point_location[2][1]) / 2 < point_location[0][1]:
        #    up_h = abs(point_location[0][1] - (point_location[1][1] + point_location[2][1]) / 2)*6 
        #else:
        #    up_h = abs(point_location[0][1] - (point_location[5][1] + point_location[6][1]) / 2)*3 
        #
        #if point_location[0][1] < (point_location[5][1] + point_location[6][1]) / 2:
        #    down_h = abs(point_location[0][1] - (point_location[5][1] + point_location[6][1]) / 2)*3
        #else:
        #    down_h = abs(point_location[0][1] - (point_location[1][1] + point_location[2][1]) / 2)*6
        
        #以鼻子为中心点计算其他特征点的距离
        distance_x =[]
        distance_y =[]
        for i in range(len(point_index)):
            if i == 0:
                continue
            distance_x.append(point_location[i][0] - point_location[0][0])
            distance_y.append(point_location[i][1] - point_location[0][1])
        
        #从各个特侦点计算脸部的大致位置
        up_h =min(50,abs(min(-15,min(distance_y))))*2
        down_h = min(50,max(15,max(distance_y)))*2
        right_w = min(50,max(15,max(distance_x)))*2
        left_w = min(50,abs(min(-15,min(distance_x))))*2
        center_point_x =  point_location[0][0]
        center_point_y =  point_location[0][1]
        #从图片中切出脸的大致位置
        img = cv2.imread(raw_pictiure_path)
        (image_max_y,image_max_x,_) = img.shape
        cut_face_image = img[max(0,int(center_point_y - up_h)):min(image_max_y,int(center_point_y + down_h)),max(0,int(center_point_x - left_w)):min(int(center_point_x + right_w),image_max_x)]
        
        #如果检测到脸的方向为横那么旋转90度
        print("-----------------face:",abs(point_location[3][0] - point_location[4][0]),(point_location[3][0] + point_location[4][0]) / 2,center_point_x)
        if abs(point_location[3][0] - point_location[4][0]) < 100:
            #眼睛在左边
            if (point_location[3][0] + point_location[4][0]) / 2 < center_point_x and (point_location[3][0] + point_location[4][0]) / 2 - center_point_x < 0:
                cut_face_image = cv2.rotate(cut_face_image, cv2.ROTATE_90_CLOCKWISE)
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            #眼睛在右边
            elif (point_location[3][0] + point_location[4][0]) / 2 > center_point_x and (point_location[3][0] + point_location[4][0]) / 2 - center_point_x > 0:
                cut_face_image = cv2.rotate(cut_face_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
         #如果检测到脸的方向倒置则进行180度旋转保证脸方向朝上
        elif (point_location[3][1] + point_location[4][1]) / 2 - center_point_y >= 30:
            cut_face_image = cv2.rotate(cut_face_image, cv2.ROTATE_180)
            img = cv2.rotate(img, cv2.ROTATE_180)
        cv2.imwrite(raw_pictiure_path, img)
        cv2.imwrite(result_PATH, cut_face_image)
        self.txt_file.close()