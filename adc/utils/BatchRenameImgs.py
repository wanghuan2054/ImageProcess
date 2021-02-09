#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:10024908
# @Version：V 0.1
# datetime:2021/1/28 14:29
# @desc : 配置指定目录路径，替换指定目录下所有图片名字中的subcode字符串
# ADC 测试集图片批量修改图片原来判图code，subcode统一脱敏后传给厂商进行测试
# 导入内置的os模块和datetime模块
import os
import datetime
import sys
import pandas as pd
import math
import shutil

# 指定图片根目录
IMAGESROOTPATH = r"E:\任务+项目\ADC\ADC POC\训练测试图片\处理后测试集\原本标签\L490J"
# IMAGESROOTPATH = r"E:\任务+项目\ADC\20201102\测试集\处理后标签\L691J"

# 指定处理完后的图片存放目录
TARGETIMAGESROOTPATH=r"E:\任务+项目\ADC\ADC POC\训练测试图片\处理后测试集\处理后标签"

# 现有图片规则，按照下划线分割，倒数第4位是subcode
SUBCODE_POSITION = 4
# 指定要替换subcode的字符串
REPLACE_STR = 'xxxxx'
# 指定分件分包的大小 , 初始大小为40M
FILE_SIZES = 40*1024*1024

# 遍历指定目录找到所有文件的大小
# 屏蔽实现文件夹下还存在文件夹的情况
# 返回值为(文件总个数,totalSize)
def getFileFolderSize(path):
    db = 0
    imgNums = 0
    # 拿到路径下所有文件和文件夹的名字
    fs = os.listdir(path)
    for f1 in fs:
        # 拼接路径和文件夹的名字，合成一个绝对路径
        next_path = os.path.join(path, f1)
        if os.path.isfile(next_path):
            db += os.path.getsize(next_path)
            imgNums = imgNums + 1
        else:
            # 判断该目录下是否存在子目录， 若存在则删除
            shutil.rmtree(next_path)
            # ret = getFileFolderSize(next_path)  # 每调用一次会返回一个db
            # db += ret
    return db

# Byte 转 KB MB GB
def take_space(number):
    if number <= 1024:
        return (str(round(number, 2)) + 'B')
    elif number > 1024 and number <= (1024 * 1024):
        return (str(round(number / 1024, 2)) + 'KB')
    elif number > (1024 * 1024) and number <= (1024 * 1024 * 1024):
        return (str(round(number / 1024 / 1024, 2)) + 'MB')
    else:
        return (str(round(number / 1024 / 1024 / 1024, 2)) + 'GB')

# 根据文件的个数和总大小，每份设置为40M （40*1024*1024） ， 可以得到每份文件的数量
def getNumsPerBatch() :
    totalSize = getFileFolderSize(IMAGESROOTPATH)
    if totalSize <= FILE_SIZES :
        return 1
    else:
        batchs = math.ceil(totalSize / (FILE_SIZES))
        return  batchs

# 判断是不是图片类型
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
# 图片分包
def splitImgsIntoDirs() :
    if not os.path.exists(IMAGESROOTPATH) :
       print("指定目录不存在 !")
       sys.exit(0)
    # 获取文件的份数和图片总量
    batchs  = getNumsPerBatch()
    # 处理图片计数器
    counter = 0
    # 获取path目录下所有的图片文件名
    img_names = os.listdir(path=IMAGESROOTPATH)
    print(IMAGESROOTPATH + ' 下共有' + str(len(img_names)) + "个文件（包括文件夹）")
    code_dict = dict()
    matrixList = []
    for img_name in img_names:
        if not is_img(os.path.splitext(img_name)[-1]) :
            continue
        counter = counter + 1
        singleImgList = []
        # 图片名全部预处理转小写
        img_name = img_name.lower()
        # replace_name = img_name.replace(img_name.split("_")[SUBCODE_POSITION],REPLACE_STR)

        #  每张图片下划线切分后的长度
        # imgNameLength =  img_name.split("_")

        absPath = os.path.join(IMAGESROOTPATH, img_name)
        # 获取文件名 , 不带后缀
        # fileName = os.path.splitext(img_name)[0]

        # 获取图片true label
        subcode = img_name.split("_")[-SUBCODE_POSITION]
        if os.path.isdir(absPath):
            continue
        elif os.path.isfile(absPath):
            replace_name = img_name.replace(subcode, REPLACE_STR)
            if subcode not in code_dict.keys():
                code_dict[subcode] = 1
            else:
                code_dict[subcode] = code_dict[subcode] + 1

            # 区分文件的名字和后缀:
            oldfilename = os.path.join(IMAGESROOTPATH, img_name)
            newfilename = os.path.join(os.path.join(TARGETIMAGESROOTPATH,IMAGESROOTPATH.split('\\')[-1]), replace_name)

            # 生成Excel 存储替换前图片名  替换后图片名  类标签
            singleImgList = [img_name ,replace_name , subcode]
            matrixList.append(singleImgList)

            # os.rename(oldfilename, newfilename)
            # print(oldfilename,newfilename)

            # 判断目标目录是否存在，不存在则创建
            if not os.path.exists(os.path.dirname(newfilename)) :
                os.makedirs(os.path.dirname(newfilename))
            shutil.copy(oldfilename,newfilename)
    print(IMAGESROOTPATH + " 目录下共替换 " + str(counter) + " 张图片")
    # # list转dataframe
    df = pd.DataFrame(matrixList, columns=['source', 'target', 'label'])
    #
    # 保存excel到IMAGESROOTPATH 下
    df.to_excel(os.path.join(TARGETIMAGESROOTPATH , IMAGESROOTPATH.split('\\')[-1]) + ".xlsx", index=False)

    print(code_dict)

# 程序入口
if __name__ == "__main__":
    print(getNumsPerBatch())
    starttime = datetime.datetime.now()
    splitImgsIntoDirs()
    endtime = datetime.datetime.now()
    print("共计耗时 ： " + str(endtime - starttime))
