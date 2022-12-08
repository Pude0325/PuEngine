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

class _Mouse(_pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = _pg.surface.Surface((1,1))
            self.rect = self.image.get_rect()
            self.mask = _pg.mask.from_surface(self.image)
        def update(self):
            self.rect.topleft = _pg.mouse.get_pos()
        def draw(self, view):
            view.blit(self.image, self.rect)

class MouseImage(_pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = _pe.Resource.GetImage('puengine' ,'mouse')
        self.rect = self.image.get_rect()
    def update(self):
            self.rect.topleft = _pg.mouse.get_pos()
    def draw(self, view):
            view.blit(self.image, self.rect)

class Screens:
    
    if _pe.System.profile['window.resizeble'] == True:
        appview = _pg.display.set_mode((1280,720), _pg.RESIZABLE)
    else: appview = _pg.display.set_mode((1280,720))
    __mouse = _Mouse()
    __mouse_image: MouseImage = None
    @staticmethod
    def GetLength(mode:str, a:_pg.surface.Surface, b:_pg.surface.Surface=None):
        """取的兩個surface物件的高度、寬度的相加或相減。\n
         - 'w+ => 寬度相加'\n
         - 'w- => 寬度相減'\n
         - 'h+ => 高度相加'\n
         - 'h- => 高度相減'\n"""
        if b == None:
            if(mode == 'w-' or mode == 'w+' or mode == 'w'):
                return a.get_size()[0]
            elif(mode == 'h-' or mode == 'h+' or mode == 'h'):
                return a.get_size()[1]
        if(mode == 'w-'):
            return a.get_size()[0] - b.get_size()[0]
        elif(mode == 'w+'):
            return a.get_size()[0] + b.get_size()[0]
        elif(mode == 'h-'):
            return a.get_size()[1] - b.get_size()[1]
        elif(mode == 'h+'):
            return a.get_size()[1] + b.get_size()[1]
    
    @staticmethod
    def Initialization():
        """初始化ScreensAPI"""
        _pg.display.set_caption(_pe.Resource.Get("puengine" ,'title'))
        _pg.display.set_icon(_pg.transform.scale(_pe.Resource.GetImage('puengine', 'icon'), (65,65)))
        _pe.Event.addEvent('update.start', Screens.__mouse.update)
        if _pe.System.profile['use_gamemouse']:
            _pg.mouse.set_visible(False)
            Screens.__mouse_image = MouseImage()     
            def mouse_update():
                Screens.__mouse_image.update()
                Screens.__mouse_image.draw(Screens.appview)
            _pe.Event.addEvent('update.stop', mouse_update)
        def screen_update():
                Screens.appview.fill((255,255,255))
        _pe.Event.addEvent('update.start', screen_update)
            


    @staticmethod
    def focusedCheck(sprite:_pg.sprite.Sprite, mode='mask'):
        """焦點檢查，檢查滑鼠是否停留在指定物件上。\n
        mode：\n
        \t    - 'mask' => 用透明像素格進行判斷(default，需要mask物件。)\n
        \t    - 'pos' => 利用Rect的座標進行判斷"""
        if mode == 'mask':
            ru = _pg.sprite.collide_mask(Screens.__mouse, sprite)
            if ru:
                return True
            else: return False
        elif mode == 'pos':
            pos = _pg.mouse.get_pos()
            if pos[0] > sprite.rect.topleft[0] and pos[0] < sprite.rect.bottomright[0]:
                if pos[1] > sprite.rect.topleft[1] and pos[1] < sprite.rect.bottomright[1]: return True
            return False

    @staticmethod
    def collideCheck(spriteA:_pg.sprite.Sprite, spriteB:_pg.sprite.Sprite, mode='mask'):
        """檢查spriteA是否與spriteB重疊"""
        if mode == 'mask':
            ru = _pg.sprite.collide_mask(spriteB, spriteA)
            if ru:
                return True
            else: return False
        elif mode == 'pos':
            ru = _pg.sprite.collide_rect(spriteA, spriteB)
            if ru: return True
            else: return False
    
    @staticmethod
    def groupCollideCheck(sprite:_pg.sprite.Sprite, group:_pg.sprite.Group, mode='mask', dokill:bool=False):
        """檢查spriteA是否與spriteB重疊"""
        if mode == 'mask':
            ru = _pg.sprite.spritecollide(sprite, group, dokill, _pg.sprite.collide_mask)
            return ru
        elif mode == 'pos':
            ru = _pg.sprite.spritecollide(sprite, group, dokill)
            return ru