# -*- coding: utf-8 -*-
# @Time      : 2023/2/24 14:05
# @Author    : JianjinL
# @eMail     : jianjinlv@163.com
# @File      : filter_labels
# @Software  : PyCharm
# @Dscription: 将生成的数据集标签与图片对一遍，删除没有图片的标签

import os
import argparse

# 1. 定义命令行解析器对象
parser = argparse.ArgumentParser(description='筛选标签')
# 2. 添加命令行参数
parser.add_argument('--img_dir', type=str, required=True, help="生成的图片所在文件夹")
parser.add_argument('--label_path', type=str, required=True, help="原始标签所在路径")
# 3. 从命令行中结构化解析参数
args = parser.parse_args()
# 解析参数
img_dir = args.img_dir
label_path = args.label_path

# 读取图片列表
img_list = set(os.listdir(img_dir))

with open(os.path.join(label_path.replace("labels.txt", "labels_filter.txt")), 'w', encoding='utf8') as f_filter:
    with open(label_path, 'r', encoding='utf8') as f_label:
        label_lines = f_label.readlines()
        for line in label_lines:
            img_name = line.split("\t")[0].split("images/")[1]
            if img_name in img_list:
                f_filter.write(line)


