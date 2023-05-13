# -*- coding: utf-8 -*-
# @Time      : 2023/2/23 12:00
# @Author    : JianjinL
# @eMail     : jianjinlv@163.com
# @File      : filter_fonts
# @Software  : PyCharm
# @Dscription: 筛选符合字典的字体
import os
import shutil
from fontTools.ttLib import TTFont
import fontTools
import argparse

# 1. 定义命令行解析器对象
parser = argparse.ArgumentParser(description='筛选符合字典的字体')
# 2. 添加命令行参数
parser.add_argument('--dict_path', type=str, required=True, help="字典路径")
parser.add_argument('--font_dir', type=str, required=True, help="字体所在文件夹")
# 3. 从命令行中结构化解析参数
args = parser.parse_args()
# 字典、字体文件夹
dict_path = args.dict_path
font_dir = args.font_dir

# 创建文件夹
if not os.path.exists(font_dir+"_filter"):
    os.mkdir(font_dir+"_filter")



# 记录结果
result = []


# 遍历每个字体
for font_path in os.listdir(font_dir):
    # 保存结果的字典
    data = {}
    # 读取字体对象
    try:
        font = TTFont(os.path.join(font_dir, font_path))
    except fontTools.ttLib.TTLibError as err:
        continue
    # 读取字典并遍历校验每个字符
    with open(dict_path, 'r', encoding='utf8') as fread:
        charlist = [char.replace("\n", "") for char in fread.readlines()]
        charset = set(charlist)
        for char in charlist:
            for table in font['cmap'].tables:
                try:
                    if ord(char) in table.cmap.keys() and char in charset:
                        charset.remove(char)
                except TypeError as err:
                    print(f"Font:{font}, Error:{err}")
        print(f"字体：{font_path}, 不支持的字符：{charset}")
        if len(charset) == 0:
            shutil.copy(os.path.join(font_dir, font_path), os.path.join(font_dir + "_filter", font_path))



