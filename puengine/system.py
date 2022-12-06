import pygame as _pg
from puengine.pures import PuRes as _pr
from puengine.event import Event as _ev
import re as _re
from puengine.pures import PuRes as _pr
from puengine.resource import Resource as _re
import puengine.command as _cmd
class Key:
    @staticmethod
    def NameToCode(name:str):
        for key, value in Key.__keyCode:
            if value == name: return key
        return None
    @staticmethod
    def CodeToName(code:str):
        return Key.__keyCode.get(code, 0)
    __keyCode = {}
    @staticmethod
    def Init():
        Key.__keyCode = _pr.Load("puengine\pur\keycode.pur", False, False)
    
class Mouse:
    @staticmethod
    def GetPos():
        return _pg.mouse.get_pos()

class System:
    class Type:
        """系統建立的事件列舉"""
        GAME_START = 'game.start'
        """遊戲開始"""
        GAME_INIT = 'game.init'
        """遊戲初始化"""
        KEY_DOWN = 'game.keydown'
        """鍵盤按鍵被點擊"""
        KEY_UP = 'game.keyup'
        """鍵盤按鍵被釋放"""
        KEY_PRESS = 'game.keypress'
        """鍵盤按鍵被按住(重複)"""
        MOUSE_MOVE = 'game.mousemove'
        """滑鼠移動"""
        MOUSE_PRESS = 'game.mousepress'
        """滑鼠按鍵被按住(重複，且只有左、中、右鍵)"""
        MOUSE_UP = 'game.mouseup'
        """滑鼠按鍵被釋放(只包含左、中、右鍵)"""
        MOUSE_DOWN = 'game.mousedown'
        """滑鼠按鍵被按下(不重複，且只有左、中、右鍵)"""
        MOUSE_WHEEL = 'game.mousewheel'
        """滑鼠滾輪被滾動"""
        UPDATE = 'game.update'
        """遊戲更新"""
        APP_CLOSE = 'app.close'
        """退出應用程式"""
        GAME_UPDATE = 'game.update'
        """每經過一遊戲刻"""
        SAVE = 'save'
        """儲存"""
        LOAD = 'load'
        """讀取"""
    
    __keypress = []
    __mousepress = [False, False, False]
    profile = {}
    """設定組，儲存遊戲當前的設定值。"""
    lang = "zh_tw"
    """遊戲初始化時使用的語言，通常用來讀取Res。"""
    FPS = 60
    """遊戲幀數，更改數值將造成嚴重後果。"""
    running = True
    CLOCK = _pg.time.Clock()

    @staticmethod
    def __keypress_load(arg):
            for k in System.__keypress:
                if k == arg['key']: return
            System.__keypress.append(arg['key'])
            _ev.send(System.Type.KEY_DOWN, {'key': arg['key']})
    @staticmethod
    def keypress_pop(arg):
        """系統用途，錯誤的調用可能造成嚴重後果。"""
        for k in System.__keypress:
            if k == arg['key']:
                System.__keypress.remove(k)
                _ev.send(System.Type.KEY_UP, {'key': arg['key']})

    @staticmethod
    def KeyEvent():
        for k in System.__keypress:
            _ev.send(System.Type.KEY_PRESS, {'key':k})

    @staticmethod
    def mouseEvent():
        """系統用途，錯誤的調用可能造成嚴重後果。"""
        for i in range(len(System.__mousepress)):
            if(System.__mousepress[i] == True):
                _ev.send(System.Type.MOUSE_PRESS, {'key': i+1})

    @staticmethod
    def quit():
        System.running = False
    

    def Initialization():
        System.profile = _pr.Load("setting.pur", True)
        System.lang = System.profile['language']
        _re.LoadSource('puengine', System.lang, defaultLang='zh_tw')

        _ev.addEvent(System.Type.GAME_INIT)
        _ev.addEvent(System.Type.GAME_START)
        _ev.addEvent(System.Type.KEY_DOWN)
        _ev.addEvent(System.Type.KEY_UP)
        _ev.addEvent(System.Type.KEY_PRESS)
        _ev.addEvent(System.Type.MOUSE_DOWN)
        _ev.addEvent(System.Type.MOUSE_MOVE)
        _ev.addEvent(System.Type.MOUSE_PRESS)
        _ev.addEvent(System.Type.MOUSE_UP)
        _ev.addEvent(System.Type.MOUSE_WHEEL)
        _ev.addEvent(System.Type.UPDATE)
        _ev.addEvent(System.Type.APP_CLOSE)
        _ev.addEvent(System.Type.GAME_UPDATE)

        _ev.addEvent(System.Type.APP_CLOSE, System.quit)
        _ev.addEvent(System.Type.KEY_PRESS, System.__keypress_load)

        def mousepress_load(args):
            System.__mousepress[args['key'] -1] = True
        def mousepress_pop(args):
            System.__mousepress[args['key'] -1] = False
        _ev.addEvent(System.Type.MOUSE_DOWN, mousepress_load)
        _ev.addEvent(System.Type.MOUSE_UP, mousepress_pop)

        '''開發者模式設定'''
        ## Print mouse pos
        def print_mouse_pos(args):
            # print(pygame.mouse.get_pos())
            _cmd.Command.delog(_pg.mouse.get_pos(), _cmd.TextColor.Black_Bright, True)
        if System.profile['developer.print_mouse_pos']: _ev.addEvent(System.Type.MOUSE_DOWN, print_mouse_pos)
        def on_off__print_mouse_pos(args):
            if args.Get(0) == 'false' or args.Get(0) == '0': _ev.removeEvent(System.Type.MOUSE_DOWN, print_mouse_pos)
            elif args.Get(0) == 'true' or args.Get(0) == '1':
                if _ev.fineEvent(System.Type.MOUSE_DOWN, print_mouse_pos) == False:
                    _ev.addEvent(System.Type.MOUSE_DOWN, print_mouse_pos)
            else: _cmd.Command.delog('print_mouse_pos {arg} is boolen', _cmd.TextColor.Red, True)
        _cmd.Command.command_register("print_mouse_pos", on_off__print_mouse_pos, _re.Get("puengine" ,"print_mouse_pos_help"))
        
        def testKey(args):
            _cmd.Command.delog(f"@{args['key']}: <n> \"{_pg.key.name(args['key'])}\";", close=True)
        _ev.addEvent(System.Type.KEY_DOWN, testKey)
        
        ## Open command function
        if System.profile['developer.open_cmd']:
            
            _cmd.Command.Initialization()
            def __startCmd(args):
                if _pg.key.get_pressed()[_pg.K_LCTRL] == True and args['key'] == _pg.K_i:
                    _cmd.Command.Input()
            _ev.addEvent(System.Type.KEY_DOWN, __startCmd)

            
            

        '''############'''