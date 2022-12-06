"""
Welcome to PuEngine!\n
EN : PuEngine is an extension engine based on pygame, designed to allow developers to develop games in a simple way, and provides standardized engine usage specifications to ensure game scalability and functional practicability.\n
\nCN : PuEngine是基於pygame的擴展引擎，旨在讓開發者以簡單的方式進行遊戲開發，並提供制式化的引擎使用規範，確保遊戲的可擴展性和功能的實用性。
"""
from puengine.system import System, Key, Mouse
System.Initialization()
from pygame.surface import Surface
from puengine.command import Command, TextColor
from puengine.event import Event
from puengine.resource import Resource
from puengine.screen import Sprite, PuStyle
from puengine.time import Time
# welcome #
Command.Clear()
Command.delog("Hello ", TextColor.Cyan_Bright)
Command.delog("developer", TextColor.Green_Bright)
Command.delog(", welcome to ", TextColor.Cyan_Bright)
Command.delog("PuEngine", TextColor.Megenta_Bright)
Command.delog("!", TextColor.Cyan_Bright, True)
# ------- #

# init #

# ---- #