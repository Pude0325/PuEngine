import puengine as _pe
import pygame as _pg

class PuStyle:
    """遊戲中用於樣式一致化的列舉類別"""
    class Font:
        @staticmethod
        def add_font(path:str, size:int):
            try:
                return _pg.font.Font(path, size)
            except:
                _pe.Command.delog(f"path: {path} is not font file.", _pe.TextColor.Red)


    class Position:
        CENTER = 'center'
        TOPLEFT = 'topleft'
        TOPRIGHT = 'topright'
        BOTTOMLEFT = 'bottomleft'
        BOTTOMRIGHT = 'bottomright'

    class Color:
        Red = (200,0,0)
        Bule = (0,0,200)
        Green = (0,200,0)
        Black = (0,0,0)
        White = (255,255,255)

class Sprite(_pg.sprite.Sprite):
    def start(self): pass
    def stop(self): pass

class Screens:
    appview = _pg.display.set_mode(_pe.System.profile['window.size'])
