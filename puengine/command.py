import os as _sys
class TextColor:
        Defalut = '\033[0m'
        White = '\033[37m'

        Black = '\033[30m'
        Red = '\033[31m'
        Green = "\033[32m"
        Yellow = "\033[33m"
        Bule = "\033[34m"
        Megenta = "\033[35m"
        Cyan = "\033[36m"

        Black_Bright = '\033[90m'
        Red_Bright = '\033[91m'
        Green_Bright = "\033[92m"
        Yellow_Bright = "\033[93m"
        Bule_Bright = "\033[94m"
        Megenta_Bright = "\033[95m"
        Cyan_Bright = "\033[96m"

class CommandArgs:
    def __init__(self, lis:list):
        self.args = lis
    def Get(self, index:int):
        try:
            return self.args[index]
        except:
            return None

class Command:
    cmd_func = {}
    cmd_help = {}
    started = False
    @staticmethod
    def Initialization():
        def help(args):
            for key in Command.cmd_help:
                Command.delog(" - ").delog(f"{key}", TextColor.Bule_Bright).delog(f" : {Command.cmd_help[key]}", close=True)
        Command.command_register('help', help)
        

    @staticmethod
    def command_register(key:str, func, help:str=None):
        if callable(func) == False: print("func is not function.")
        else: 
            Command.cmd_func[key] = func
            if help != None:
                Command.cmd_help[key] = help

    @staticmethod
    def runcmd(c:list):
        t = c.pop(0)
        if Command.cmd_func.get(t) != None:
            Command.cmd_func.get(t)(CommandArgs(c))
        else:
            Command.delog("Not fine command.", TextColor.Red, True)
    
    @staticmethod
    def Input():
        if Command.started == False:
            Command.started = True
            c = input('=>')
            cs = c.split(' ')
            Command.started = False
            Command.runcmd(cs)

    
    @staticmethod
    def delog(context:str, color:str=TextColor.Defalut, close:bool=False):
        if Command.started == False:
            if close:
                print(f'{color}{context}{TextColor.Defalut}')
            else:
                print(f'{color}{context}{TextColor.Defalut}', end='')
        return Command

    @staticmethod
    def Clear():
        _sys.system('CLS')

