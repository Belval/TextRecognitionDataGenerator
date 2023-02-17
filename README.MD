# TextRecognitionDataGenerator 



[English](README_EN.md) | 简体中文

## 介绍

一个文字识别模型的数据生成器

## 特性

1. 支持中英文识别。

## 必要条件

- Python 3.6+

## 近期更新

**`2023-02-15`**: 继承自[TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator) 。

## 内容

- [安装](#安装)
    - [python](#python)
    - [docker](#docker)
- [使用](#使用)
    - [训练](#训练)
    - [测试](#测试)
    
## 安装
创建虚拟环境
```commandline
conda create -n TextRecognitionDataGenerator python=3.7
```
激活虚拟环境
```commandline
conda activate TextRecognitionDataGenerator
```

安装所需以来
```commandline
pip install -r requirements.txt
```
## 使用
在项目根目录下，执行生成语句，
```commandline
bash run.sh
```

对于不同语言的生成需求可对如下参数进行调整，

***参数配置表***

|     参数     |                            含义                            |  类型   |    默认值    |
| :----------: | :--------------------------------------------------------: | :-----: | :----------: |
| --output_dir |                       结果输出文件夹                       |   str   |     out/     |
|      -i      |                     指定生成的文本语料                     |   str   |              |
|      -l      |                            语言                            |   str   |      en      |
|      -c      |                       生成的图片数量                       |   int   |              |
|     -rs      |     使用随机字符组合作为语料，即没有语义信息的文本组合     |         |              |
|     -let     |    与-rs一起使用，使用随机字符组合作为语料，只生成字符     |         |              |
|     -num     |    与-rs一起使用，使用随机字符组合作为语料，只生成数字     |         |              |
|     -sym     |    与-rs一起使用，使用随机字符组合作为语料，只生成标点     |         |              |
|      -w      |                  生成图片中包含的单词数量                  |   int   |      1       |
|      -r      |           与-w搭配使用，随机生成单词数，最大为-w           |         |              |
|      -f      |                     设置图片高度像素数                     |   int   |      32      |
|      -t      |                        执行的进程数                        |   int   |      1       |
|      -e      |                      设置图片保存格式                      |   str   |     jpg      |
|      -k      |      文本行倾斜角度,需要与-rk一起使用，否则为固定角度      |   int   |      0       |
|     -rk      |            使得倾斜角度为，-k到+k的范围随机选取            |         |              |
|     -wk      |              使用维基百科语料，运行似乎会报错              |         |              |
|     -bl      |  增加高斯模糊效果，数值越大越模糊，设置-rbl模糊程度可随机  |   int   |      0       |
|     -rbl     |               随机模糊，模糊值从0到-bl的数值               |         |              |
|      -b      |     背景，0：高斯噪点，1：白色背景，2：类网格，3：图片     |         |              |
|     -hw      |                                                            |         |              |
|     -na      |                                                            |         |              |
|     -om      |                                                            |         |              |
|     -obb     |                                                            |         |              |
|      -d      | 添加文字扭曲效果，0：无变换，1：Sine，2：Cosine，3：random |   int   |      0       |
|     -do      |                                                            |         |              |
|     -wd      |                                                            |         |              |
|     -al      |                                                            |         |              |
|     -or      |           生成的文字方向，0代表水平，1代表竖直的           |         |              |
|     -tc      |  设置文本颜色，设置一个颜色区间的话形如'#000000,#888888'   |   str   |   #282828    |
|     -sw      |      两个词之前的空间,1.0代表一个空格，0代表没有间隔       |  float  |     1.0      |
|     -cs      |                                                            |         |              |
|  --margins   |               设置文本行四周边距，单位是像素               | margins | (5, 5, 5, 5) |
|    --fit     |    加这个参数将使边距更紧密，一般配合--margins一起使用     |         |              |
|     -ft      |                                                            |         |              |
|     -fd      |                                                            |         |              |
|     -id      |                                                            |         |              |
|     -ca      |                                                            |         |              |
|     -dt      |                                                            |         |              |
|     -stw     |                                                            |         |              |
|     -stf     |                                                            |         |              |
|     -im      |                                                            |         |              |





## 联系

1. 邮箱：jianjinlv@163.com

## 许可证书

本项目的代码基于MIT协议发布。