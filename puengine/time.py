import puengine as _pe
import math as _ma
class Time:
    time = 0
    @staticmethod
    def Init():
        pass
    @staticmethod
    def add_time(t:int=1):
        for i in range(t):
            Time.time += 1
            _pe.Event.send(_pe.System.Type.GAME_UPDATE)

    @staticmethod
    def Get(mode:str='date'):
        if mode == 'date':
            ru = {
                'year':_ma.floor(Time.time / 1440),
                'month':_ma.floor(Time.time % 1440 / 120),
                'day':_ma.floor(Time.time % 120 / 4),
                'period':_ma.floor(Time.time % 4)
            }

        elif mode == 'through':
            return {
                'year':_ma.floor(Time.time / 1440),
                'month':_ma.floor(Time.time / 120),
                'day':_ma.floor(Time.time / 4),
                'period':Time.time
            }

