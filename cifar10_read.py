#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: cifar10_read.py
# Author: Yahui Liu <yahui.cvrs@gmail.com>

import cPickle

def unpickle(file):
  with open(file, 'rb') as fo:
    dict = cPickle.load(fo)
  return dict

if __name__ == '__main__':
  print(unpickle('/workspace/CIFAR-master/bin_test/test_batch'))
