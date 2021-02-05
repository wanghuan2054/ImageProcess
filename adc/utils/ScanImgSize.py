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

# 路径名中不能出现中文
imagePath = r"C:\Users\10024908\Desktop\L691J"

# IMAGESROOTPATH = r"E:\任务+项目\ADC\20201102\测试集\处理后标签\L691J"

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
view_size = dict()
index = 0
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

   # size = str(img.shape[0])+"_"+str(img.shape[1])
   print(os.path.join(imagePath,x))
   print( str(img.shape[0])+ " " + str(img.shape[1]))
   # index = index + 1
   # print(view_size.keys())
   # if size not in view_size.keys():
   #    view_size[size] = 1
   # else:
   #    view_size[size] = view_size[size] + 1

# print(view_size)