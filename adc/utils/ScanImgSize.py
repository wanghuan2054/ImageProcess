#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
    @version:
    author:wanghuan
    @time: 2021/01/30
    @file: ScanImgSize.py
    @desc :
"""
import cv2
import  os
imagePath = r"C:\Users\wanghuan\Desktop\12345";

def is_img(ext):
 ext = ext.lower()
 if ext == '.jpg':
  return True
 elif ext == '.png':
  return True
 elif ext == '.jpeg':
  return True
 elif ext == '.bmp':
  return True
 else:
  return False
# 遍历指定目录集
for x in os.listdir(imagePath):
 # 获取文件后缀名
 if is_img(os.path.splitext(x)[1]):
   # 读取图像
   img = cv2.imread(os.path.join(imagePath,x))
   # 打印图像的分辨率
   # (3840, 2160, 3)
   # height(rows) of image
   # width(colums) of image
   # the pixels value is made up of three primary colors
   print(img.shape[0] , img.shape[1])