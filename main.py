"""應用程式入口"""
import pygame
pygame.init()
import puengine

if __name__ == '__main__':
    # 遊戲迴圈和初始化
    while (puengine.System.running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                puengine.System.quit()
            elif event.type == pygame.KEYDOWN:
                puengine.Event.send(puengine.System.Type.KEY_PRESS, {"key":event.key})
            elif event.type == pygame.KEYUP:
                puengine.System.keypress_pop({"key":event.key})
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1 or event.button == 2 or event.button == 3):
                    puengine.Event.send(puengine.System.Type.MOUSE_DOWN, {'key': event.button})
                elif event.button == 4:
                    puengine.Event.send(puengine.System.Type.MOUSE_WHEEL, {'key': 'up'})
                elif event.button == 5:
                    puengine.Event.send(puengine.System.Type.MOUSE_WHEEL, {'key': 'down'})
            elif event.type == pygame.MOUSEBUTTONUP:
                if (event.button == 1 or event.button == 2 or event.button == 3):
                    puengine.Event.send(puengine.System.Type.MOUSE_UP, {'key': event.button})
            elif event.type == pygame.MOUSEMOTION:
                puengine.Event.send(puengine.System.Type.MOUSE_MOVE, {'pos': event.pos})
        puengine.System.mouseEvent()
        ######################################################################
        puengine.Event.send(puengine.System.Type.UPDATE)
        ######################################################################
        puengine.System.CLOCK.tick(puengine.System.FPS)
        pygame.display.update()

    pygame.quit()
    puengine.Event.APP_CLOSE()