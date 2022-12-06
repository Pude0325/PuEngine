from threading import Thread as _thread
import sys as _sys
from puengine.command import Command as _cmd, TextColor as _ts

class Event:
    eventlist = {}
    @staticmethod
    def Initialization():
        pass

    @staticmethod
    def addEvent(eventType:str, func=None):
        """新增事件進入系統中，不設置func時只建立空的事件組。"""
        if (func != None and callable(func) == False): 
            _cmd.delog("The \"func\" of the event registration should be a method", _ts.Red, True)
            return
        if (Event.eventlist.get(eventType) == None):
            Event.eventlist[eventType] = []
        if func != None:
            Event.eventlist[eventType].append(func)
    
    @staticmethod
    def removeEvent(eventType:str, func=None):
        """刪除事件，或清空事件組。"""
        if (Event.eventlist.get(eventType) == None): return
        if (func == None): 
            Event.eventlist[eventType].clear()
            return
        elif (callable(func) == True):
            try:
                Event.eventlist[eventType].remove(func)
            except: return

    @staticmethod
    def fineEvent(eventType:str, func):
        """尋找指定事件是否已存在"""
        if (eventType == None and func == None): return False
        elif (Event.eventlist.get(eventType) == None): return False
        elif (eventType == None and func != None):
            for key, lis in Event.eventlist:
                for i in lis:
                    if Event.eventlist[key][i] == func:
                        return True
            return False
        elif (eventType != None and func == None):
            if  Event.eventlist.get(eventType) == True:
                return True
            else: False
        else:
            for i in Event.eventlist[eventType]:
                if i == func:
                    return True
            return False


    @staticmethod
    def send(eventType:str, args:dict=None):
        """發送事件廣播"""
        if (Event.eventlist.get(eventType) == None): return
        if (args == None):
            for ev in Event.eventlist[eventType]:
                th = _thread(target=ev)
                th.daemon = True
                th.start()
        else:
            for ev in Event.eventlist[eventType]:
                th = _thread(target=ev, args=(args,))
                th.daemon = True
                th.start()

    @staticmethod
    def APP_CLOSE():
        _sys.exit()


    