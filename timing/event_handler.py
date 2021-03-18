from abc import ABC, abstractmethod

from math import floor
from time import time

import pygame
import pygame.freetype

class EventHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def no_touch_no_motion_event(self):
        pass

    @abstractmethod
    def motion_no_touch_event(self):
        pass

    @abstractmethod
    def touch_event(self):
        pass

    @abstractmethod
    def touch_motion_event(self):
        pass

    @abstractmethod
    def motion_event(self):
        pass

    @abstractmethod
    def no_motion_event(self):
        pass


class PyGameVisualizer(EventHandler):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        
        self.large_font = pygame.freetype.SysFont('Calibri', 100)
        self.medium_font = pygame.freetype.SysFont('Calibri', 50)

        self.time_tracking = {
            0: [],
            1: []
        }
        self.count_down_start = 38*60
        self.start_time = 0
        self.current_team = 1
        self.current_state = 'No Touch and no Motion'
        
        self.state_machine_image = {}
        self.load_images()

    @staticmethod
    def format_seconds(total_seconds):
        t = floor(total_seconds)
        hours = (t // 3600)
        minutes = (t // 60) % 60
        seconds = t % 60

        return hours, minutes, seconds

    def load_images(self):
        self.state_machine_image['No Touch and no Motion'] = pygame.image.load('StateMachine/state_machine_no_touch_no_motion.gv.png')
        self.state_machine_image['Touch'] = pygame.image.load('./StateMachine/state_machine_touch.gv.png')
        self.state_machine_image['Motion and no Touch'] = pygame.image.load('./StateMachine/state_machine_motion_no_touch.gv.png')
        self.state_machine_image['Touch and Motion'] = pygame.image.load('./StateMachine/state_machine_touch_motion.gv.png')
        self.state_machine_image['Motion'] = pygame.image.load('./StateMachine/state_machine_motion.gv.png')
        self.state_machine_image['No Motion'] = pygame.image.load('./StateMachine/state_machine_no_motion.gv.png')

    def render_state_machine(self):
        self.screen.blit(self.state_machine_image[self.current_state], (0, 0))

    def render(self):
        for team, scores in self.time_tracking.items():
            test = []
            additional_time = 0
            for pair in scores:
                if len(pair) == 2:
                    start, stop = pair
                    test.append(stop-start)
                else:
                    additional_time = time() - self.start_time
            if team == int(self.current_team):
                color = (0, 0, 0)
                total_seconds = self.count_down_start - additional_time - sum(test)
            else:
                total_seconds = self.count_down_start - sum(test)
                color = (97, 97, 97)
            _, minutes, seconds = PyGameVisualizer.format_seconds(total_seconds)
            self.large_font.render_to(self.screen, (40 + 400*team, 500), f'{minutes:02.0f}:{seconds:02.0f}', color)
        self.render_state_machine()
        
        self.medium_font.render_to(self.screen, (300, 100), f'{self.current_state}', (0, 0, 0))

    def start_timer(self):
        self.time_tracking[self.current_team].append([time()])

        self.start_time = time()

    def stop_timer(self):
        if len(self.time_tracking[self.current_team]):
            self.time_tracking[self.current_team][-1].append(time())

            self.current_team = not self.current_team

    def no_touch_no_motion_event(self):
        if self.current_state != 'Touch' and self.current_state != 'Motion and no Touch':
            self.start_timer()
        self.current_state = 'No Touch and no Motion'

    def motion_no_touch_event(self):
        self.current_state = 'Motion and no Touch'

    def touch_event(self):
        self.current_state = 'Touch'

    def touch_motion_event(self):
        self.current_state = 'Touch and Motion'

    def motion_event(self):
        self.current_state = 'Motion'
        self.stop_timer()

    def no_motion_event(self):
        self.current_state = 'No Motion'
