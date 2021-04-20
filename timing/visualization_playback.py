import pygame
import pygame.freetype

from time import sleep


from ble_usb_handler import CommunicationThread
from event_handler import EventHandler, PyGameVisualizer
from timing_logic import StateMachine


class DummyCommunicationThread(CommunicationThread):
    def run(self):
        blue_team = 128
        touch = 1
        motion = 2
        
        sleep(5)
        sequence = [
            # BLUE
            (blue_team + touch, 25), # touch
            (blue_team + touch + motion, 106), # motion
            (blue_team + motion, 130), # no touch
            (blue_team, 193), # no motion 
            (blue_team + motion, 194), # motion
            (blue_team, 205), # no motion

            # GREEN
            (motion, 292), # motion
            (0, 294), # no motion
            (motion, 321), # motion
            (0, 388), # no motion
            (motion, 393), # motion
            (0, 397), # no motion
            (motion, 411), # motion
            (0, 415), # no motion
            (touch, 442), # touch
            (touch + motion, 458), # touch motion

            (touch, 528), # touch no motion
            (touch + motion, 535), # touch motion
            (touch, 538), # touch no motion
            (touch + motion, 560), # touch motion

            (blue_team + motion, 586), # motion # BLUE
            
            (motion, 592), # motion

            (blue_team, 598), # no motion BLUE
            (blue_team + motion, 601), # motion BLUE
            (blue_team, 603), # no motion BLUE
            (blue_team + motion, 604), # motion BLUE
            (blue_team, 609), # no motion BLUE
            (blue_team + motion, 613), # motion BLUE
            (blue_team, 614), # no motion BLUE
            (blue_team + motion, 616), # motion BLUE
            (blue_team, 621), # no motion BLUE
            (blue_team + motion, 622), # motion BLUE
            (blue_team, 628), # no motion BLUE
            (blue_team + motion, 631), # motion BLUE

            (0, 649), # no motion GREEN
            (motion, 652), # motion GREEN
            (0, 655), # no motion GREEN
            (motion, 659), # motion GREEN
            (0, 661), # no motion GREEN

            (blue_team, 709), # no motion BLUE
            (blue_team + motion, 719), # motion BLUE
            (blue_team, 720), # no motion BLUE
        ]
        previous = 0
        for value, frame in sequence:
            sleep((frame-previous)/30)
            self.queue.put(value)  
            
            previous = frame

if __name__ == '__main__':
    pygame.display.set_caption('Curling Timer')
    programIcon = pygame.image.load('CurlingStoneIcon.png')
    pygame.display.set_icon(programIcon)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.init()
    print(pygame.display.list_modes())

    communication_thread = DummyCommunicationThread()
    pygame_handler = PyGameVisualizer(screen)
    event_handlers = (pygame_handler, )

    state_machine = StateMachine(event_handlers=event_handlers)

    running = True
    while running:    
        screen.fill((255, 255, 255))

        if not communication_thread.queue.empty():
            item = communication_thread.queue.get_nowait()
            state_machine.run(item)

        pygame_handler.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if state_machine.motion_list:
                        state_machine.remove_motion_table(state_machine.motion_list[-1])
                
        pygame.display.flip()

    pygame.quit()
