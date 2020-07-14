# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:07:06 2020

@author: admin1
"""
import cv2

cap = cv2.VideoCapture('https://192.168.1.7:8080/video')

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break