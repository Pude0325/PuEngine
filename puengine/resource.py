
from puengine.pures import PuRes as _PuRes
import puengine.command as _cmd
import os as _os
import re as _re
import pygame as _pygame


class Resource:
    __allRes = {}
    
    @staticmethod
    def __load(packageName, lang):
        """讀取pur檔案，packageName為目錄名稱，通常與模組id相同，lang則為讀取的語言類型，"""
        ru = {}
        filedict_lang = None
        filedict_univ = None
        try:
            filedict_lang = _os.walk(f"resource\\{packageName}\\languages\\{lang}")
        except FileNotFoundError as e:
            pass
        try:
            filedict_univ = _os.walk(f"resource\\{packageName}\\universal")
        except FileNotFoundError as e:
            pass
        if filedict_lang != None:
            for p, ds, fs in filedict_lang:
                for f in fs:
                    if (_re.match(r".*\.pur", f)):
                        ru.update(_PuRes.Load(_os.path.join(p, f), False, False))
        if filedict_univ != None:
            for p, ds, fs in filedict_univ:
                for f in fs:
                    if (_re.match(r".*\.pur", f)):
                        ru.update(_PuRes.Load(_os.path.join(p, f), False, False))
        return ru

    @staticmethod
    def LoadSource(packageName, lang, defaultLang=None):
        """讀取語言文件，並加入至系統（通常根據遊戲中設定的語言讀取。）"""
        if Resource.__allRes.get(packageName) == None:
            Resource.__allRes[packageName] = {}
        if defaultLang != None:
            Resource.__allRes[packageName].update(Resource.__load(packageName, defaultLang))
        Resource.__allRes[packageName].update(Resource.__load(packageName, lang))

    
        

    @staticmethod
    def Get(packageName, key):
        """取得資源。"""
        if Resource.__allRes.get(packageName) == None:
            _cmd.Command.delog(f"{packageName}", _cmd.TextColor.Cyan_Bright)
            _cmd.Command.delog(f" not loaded", _cmd.TextColor.Red, True)
            return 'undefined'
        ru = Resource.__allRes[packageName].get(key, 'undefined')
        return ru

    def GetImage(packageName, key):
        if Resource.__allRes.get(packageName) == None:
            try:
                return _pygame.image.load(Resource.Get(packageName, key))
            except:
                _cmd.Command.delog(f"Image: ", _cmd.TextColor.Red).delog(f"{key}", _cmd.TextColor.Bule).delog(f" is not fine.", _cmd.TextColor.Red, True)
                ru = _pygame.surface.Surface((20,20))
                ru.fill((100,0,50))
                return ru
        else:
            _cmd.Command.delog(f"Image: ", _cmd.TextColor.Red).delog(f"{key}", _cmd.TextColor.Bule).delog(f" is not fine.", _cmd.TextColor.Red, True)
            ru = _pygame.surface.Surface((20,20))
            ru.fill((100,0,50))
            return ru