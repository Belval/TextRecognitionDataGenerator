# 阿拉伯语
# python trdg/run.py -c 1000000 -f 64 -b 3 -d 1 -l ar -na 2  -k 5 -rk -bl 1 -rbl -t 8 -b 3 -tc '#000000,#888888' -dt trdg/chars/ar_dict.txt -i trdg/texts/ar/train.txt -fd trdg/fonts/ar_filter/ --output_dir ar_TextRecognitionDataGenerator_train_100w
# 俄语
python trdg/run.py -c 100 -f 64 -b 3 -d 1 -l ru -na 2  -k 5 -rk -bl 1 -rbl -t 8 -b 3 -tc '#000000,#888888' --margins 0,5,0,5 --fit -dt trdg/chars/cyrillic_dict.txt -i trdg/texts/ru/train.txt -fd trdg/fonts/ru_filter/ --output_dir output/ru_TextRecognitionDataGenerator_train_100w
