#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: demo.py
# Author: Yahui Liu <yahui.cvrs@gmail.com>

import os, cv2
from pickled import *
from load_data import *

data_path = ''
file_list = 'data/cow_jpg_train.lst' #上一步生成的图片路径文件
save_path = 'bin'

if __name__ == '__main__':
  data, label, lst = read_data(file_list, data_path, shape=32)
  pickled(save_path, data, label, lst, bin_num = 4)#bin_num为生成的batch数量


