from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode
import os 

def has_glyph(font, glyph):
    for table in font['cmap'].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False

list_of_s_char = ['a','á', 'b', 'c', 's', 'd', 'z', 'e', 'é', 'f', 'g' ,'g','y', 'h' ,'i', 'í','j', 'k', 'l', 'm', 'n', 'o', 'ó' ,'ö' ,'ő', 'p', 'q' ,'r', 't' ,'u' ,'ú' ,'ü', 'ű', 'v' ,'w' ,'x' ,'y', 'z']
list_of_c_char = ['Ä','Á','B', 'C', 'D', 'E', 'É', 'F', 'G', 'H', 'I', 'Í', 'J' ,'K', 'L' , 'M' ,'N', 'O', 'Ó', 'Ö', 'Ő', 'P', 'Q', 'R', 'S', 'T', 'U', 'Ú', 'Ü' ,'Ű' ,'V' ,'W', 'X' ,'Y','Z']

path = '/home/ngyongyossy/mohammad/trdghm/TextRecognitionDataGeneratorHuMu23/trdg/fonts/hu/'
fonts_list =  ['testedCloud Calligraphy - TTF.ttf', 
               'testedAttic.ttf', 'testedTheOnlyException.ttf',
               'testedWolgast Script.ttf', 'testedPretty_City_Kitties.ttf',
               'testedcoolvetica condensed rg.ttf', 'testedCalledliner.ttf',
               'testedI Miss Your Kiss - TTF.ttf', 'testedHello Heartache - TTF.ttf',
               'testedLemon Tuesday.ttf', 'testedMiama.ttf', 
               'testedStarsFromOurEyes.ttf', 'testedBasically Yes - TTF.ttf',
               'testedComicDylans.ttf', 'testedThe Illusion of Beauty - TTF.ttf',
               'testedKiss Me or Not - OTF.ttf', 'testedGruenewald VA 1K.ttf',
               'testedAHundredMiles.ttf', 'testedgargle cd it.ttf', 
               'testedcoolvetica crammed rg.ttf', 'testedCaveat-Bold.ttf', 
               'testedRomanesco-Regular.ttf', 'testedSeaportScript-Regular.ttf', 
               'testedSacramento-Regular1.ttf', 'testedKGManhattanScript.ttf', 
               'testedSKYLINE thin.ttf', 'testedCongrats Script - TTF.ttf',
               'testedAYearWithoutRain.ttf', 'testedKGTheFighter.ttf', 
               'testedgargle cd bd it.ttf', 'testedgargle cd bd.ttf', 
               'testedDiscoverBeauty.ttf', 'testedUnicorn Confetti.ttf', 
               'testedgargle cd rg.ttf', 'testedJandaRomantic.ttf', 
               'testedKiss Me or Not - TTF.ttf', 'testedMontez-Regular.ttf', 
               'testedA Perfect Place - TTF.ttf', 'testedgargle ex bd it.ttf',
               "testedThe Miller's Free Trial.ttf", 'testedgargle rg it.ttf',
               'testedCute Little Sheep.ttf', 'testedAttic1.ttf', 
               'testedFrosting-for-Breakfast_regular.ttf', 
               'testedSKYLINE regular.ttf', 'testedWinter in March.ttf',
               'testedUnicorn Giggles - TTF.ttf', 'testedgargle bd.ttf', 
               'testedgargle bd it.ttf', 'testedSilent Fighter.ttf', 
               'testedAulyars Regular.ttf', 'testedKind Handwriting.ttf', 
               'testedgargle ex rg.ttf', 'testedSerotonin.ttf', 
               'testedSacramento-Regular.ttf', 'testedPWShesAmazing.ttf',
               'testedAnastasia.ttf', 'testedJandaScrapgirlDots.ttf',
               'testedJandaAmazingGrace.ttf', 'testedlady.ttf', 
               'testedDecember Calligraphy - TTF.ttf', 'testedAulyars Italic.ttf',
               'testedHalloween Horoscope.ttf', 'testedMermaid Confetti.ttf', 
               'testedBrillianthre.ttf', 'testedBabylonica-Regular.ttf', 
               'testedBreetty Italic.ttf', 'testedHandycheera Regular.ttf', 
               'testedKGOnlyHuman.ttf', 'testedStika Font.ttf', 
               'testedOur First Kiss.ttf', 'testedKGLegacyofVirtue.ttf', 
               'testedGruenewald VA normal.ttf', 'testedRotterland.ttf', 
               'testedCaveat-Regular.ttf', 'testedBlodwen.ttf', 
               'testedBelagia-Demo.ttf', 'testedRonaldsonGothicLicht.ttf',
               'testedCedarville-Cursive.ttf', 'testedBreetty Regular.ttf',
               'testedJandaQuickNote.ttf', 'testedzai_NicolasSloppyPen.ttf',
               'raustila-Regular.ttf', 'testedCornwall.ttf', 
               'testedGalaxy Boy - TTF.ttf', 'testedGruenewald VA 3K.ttf',
               'testedgargle ex bd.ttf', 'testedKavivanar-Regular.ttf', 
               'testedAllema Free Demo.ttf', 'testedKalam-Light.ttf', 
               'testedAffectionately Yours - TTF.ttf', 'testedKalam-Regular.ttf',
               'testedgargle ex it.ttf', 'testedcoolvetica compressed hv.ttf',
               'testedTexas Twilight.ttf', 'testedyoufoundme.ttf',
               'testedcoolvetica rg.ttf', 'testedcoolvetica rg it.ttf', 
               'RonaldsonGothic.ttf', 'testedKGGodGaveMeYou.ttf',
               'testedI Love Glittermas.ttf', 'testedAbu Dhabi .ttf',
               'testedKind and Witty - TTF.ttf', 'testedSCRIPTIN.ttf',
                'testedLittleFunnyScript.ttf']# os.listdir(path)
print(f'We are testing : {len(fonts_list)} fonts', fonts_list)
fonts_list1 = fonts_list[50:59]

# 1- Test small letters case
print('Test small letters case\n')
for font in range(len(fonts_list1)):
 print('We are Testing font :: ',fonts_list1[font])
 font = TTFont(path+fonts_list[font])

 for idx in list_of_s_char:
    print(idx, has_glyph(font,idx ))


# 2 - Test captial letters case
print('2 - Test captial letters case')
for font in range(len(fonts_list1)):
 print('We are Testing font :: ',fonts_list1[font])
 font = TTFont(path + fonts_list1[font])

 for idx in list_of_c_char:
    print(idx, has_glyph(font,idx ))
