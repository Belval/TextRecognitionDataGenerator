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

### 准备材料

- **背景**

为丰富生成图片的背景，请自行准备背景图片并放置于[images](./trdg/images)文件夹下。

- **语料**

准备文字生成语料，并放置在[texts](./trdg/texts)文件夹下，同时执行生成命令中，使用-i参数指定语料文件路径。

- **字体**

1. 需准备一个语料字典文件放置于[chars](./trdg/chars)文件夹下，该字典文件记录了生成语料中可能出现所的所有字符。
2. 下载对应语言所需要的字体文件，并放置于[fonts](./trdg/fonts)文件夹下。下面列举几个可供选择的字体下载网站： [FFONTS](https://cn.ffonts.net/Agra.font.download)、[FONT MEME](https://fontmeme.com/ziti/thai-fonts/1/)、[fontriver](https://cn.fontriver.com/foreign_look/russian/)。
3. 执行下述语句，筛选可用字体，执行完成后会在[fonts](./trdg/fonts)文件夹下生成一个带_filter后缀的文件夹，该文件夹下字体即为可用字体。

```bash
python tools/filter_fonts.py --dict_path 字典文件路径 --font_dir 字体文件夹路径
```

### 执行生成数据

在项目根目录下，执行生成语句，
```bash
bash run.sh
```

对于不同语言的生成需求可对如下参数进行调整，

***参数配置表***

|     参数     |                             含义                             |  类型   | 默认值  |
| :----------: | :----------------------------------------------------------: | :-----: | :-----: |
| --output_dir |                        结果输出文件夹                        |   str   |  out/   |
|      -i      |                      指定生成的文本语料                      |   str   |         |
|      -l      |                             语言                             |   str   |   en    |
|      -c      |                        生成的图片数量                        |   int   |         |
|     -rs      |      使用随机字符组合作为语料，即没有语义信息的文本组合      |         |         |
|     -let     |     与-rs一起使用，使用随机字符组合作为语料，只生成字符      |         |         |
|     -num     |     与-rs一起使用，使用随机字符组合作为语料，只生成数字      |         |         |
|     -sym     |     与-rs一起使用，使用随机字符组合作为语料，只生成标点      |         |         |
|      -w      |                   生成图片中包含的单词数量                   |   int   |    1    |
|      -r      |            与-w搭配使用，随机生成单词数，最大为-w            |         |         |
|      -f      |                      设置图片高度像素数                      |   int   |   32    |
|      -t      |                         执行的进程数                         |   int   |    1    |
|      -e      |                       设置图片保存格式                       |   str   |   jpg   |
|      -k      |       文本行倾斜角度,需要与-rk一起使用，否则为固定角度       |   int   |    0    |
|     -rk      |             使得倾斜角度为，-k到+k的范围随机选取             |         |         |
|     -wk      |               使用维基百科语料，运行似乎会报错               |         |         |
|     -bl      |   增加高斯模糊效果，数值越大越模糊，设置-rbl模糊程度可随机   |   int   |    0    |
|     -rbl     |                随机模糊，模糊值从0到-bl的数值                |         |         |
|      -b      |      背景，0：高斯噪点，1：白色背景，2：类网格，3：图片      |         |         |
|     -hw      |                   手写配置，当前运行会报错                   |         |         |
|     -na      | 标签输出格式，0: [TEXT]_[ID].[EXT], 1: [ID]_[TEXT].[EXT] 2: labels.txt |   int   |    0    |
|     -om      |               是否返回遮掩的图片，0：否；1：是               |   int   |    0    |
|     -obb     | 返回每个字的坐标信息，0：不返还；1：txt格式；2：Tesseract格式 |   int   |    0    |
|      -d      |  添加文字扭曲效果，0：无变换，1：Sine，2：Cosine，3：random  |   int   |    0    |
|     -do      |   定义扭曲的方向，与-d配合使用；0：上下，1：左右，2:都有。   |   int   |    0    |
|     -wd      |                       设置固定图片宽度                       |   int   |   -1    |
|     -al      | 设置文字在图片中的对其方式，需配合-wd使用，0：左，1：中，2：右。 |         |         |
|     -or      |            生成的文字方向，0代表水平，1代表竖直的            |         |         |
|     -tc      |   设置文本颜色，设置一个颜色区间的话形如'#000000,#888888'    |   str   | #282828 |
|     -sw      |       两个词之前的空间,1.0代表一个空格，0代表没有间隔        |  float  |   1.0   |
|     -cs      |             两个字符之前的空间，2代表两个像素。              |   int   |    0    |
|  --margins   |        设置文本行四周边距，单位是像素；上，左，下，右        | margins | 5,5,5,5 |
|    --fit     |     加这个参数将使边距更紧密，一般配合--margins一起使用      |         |         |
|     -ft      |                         指定某个字体                         |         |         |
|     -fd      |                     指定字体所在的文件夹                     |         |         |
|     -id      |                   指定背景图片所在的文件夹                   |         |         |
|     -ca      |   指定只生成大写或者小写的语料，upper：大写，lower：小写。   |   str   |         |
|     -dt      |                           指定字典                           |         |         |
|     -stw     |                        定义笔画的宽度                        |   int   |    0    |
|     -stf     |        定义笔画轮廓的颜色，如果stroke_width比0大的话         |   str   | #282828 |
|     -im      | 定义要使用的图像模式。RGB是默认的，L表示8位灰度图像，等等。  |   str   |   RGB   |

## 联系

1. 邮箱：jianjinlv@163.com

## 许可证书

本项目的代码基于MIT协议发布。