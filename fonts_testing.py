from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode
import os 

def has_glyph(font, glyph):
    return any(ord(glyph) in table.cmap.keys() for table in font['cmap'].tables)

list_of_s_char = ['a','á', 'b', 'c', 's', 'd', 'z', 'e', 'é', 'f', 'g' ,'g','y', 'h' ,'i', 'í','j', 'k', 'l', 'm', 'n', 'o', 'ó' ,'ö' ,'ő', 'p', 'q' ,'r', 't' ,'u' ,'ú' ,'ü', 'ű', 'v' ,'w' ,'x' ,'y', 'z']
list_of_c_char = ['Ä','Á','B', 'C', 'D', 'E', 'É', 'F', 'G', 'H', 'I', 'Í', 'J' ,'K', 'L' , 'M' ,'N', 'O', 'Ó', 'Ö', 'Ő', 'P', 'Q', 'R', 'S', 'T', 'U', 'Ú', 'Ü' ,'Ű' ,'V' ,'W', 'X' ,'Y','Z']

path = '/home/ngyongyossy/mohammad/trdghm/TextRecognitionDataGeneratorHuMu23/trdg/fonts/hu/'
fonts_list =  os.listdir(path)
print(f'We are testing : {len(fonts_list)} fonts', fonts_list)


# 1- Test small letters case
print('Test small letters case\n')
for font in range(len(fonts_list)):
 print('We are Testing font :: ',fonts_list[font])
 font = TTFont(path+fonts_list[font])

 for idx in list_of_s_char:
    print(idx, has_glyph(font,idx ))


# 2 - Test captial letters case
print('2 - Test captial letters case')
for font in range(len(fonts_list)):
 print('We are Testing font :: ',fonts_list[font])
 font = TTFont(path + fonts_list[font])

 for idx in list_of_c_char:
    print(idx, has_glyph(font,idx ))
