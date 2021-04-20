from abc import ABC, abstractmethod

from math import floor
from time import time

import subprocess

import pygame
import pygame.gfxdraw
import pygame.freetype

import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'stoneDetection')))
from stoneDetection.curling import takePicture


class EventHandler(ABC):
    def __init__(self):
        self.motion_table = {}

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

    def motion_table_update(self, motion_table):
        self.motion_table = motion_table

class PyGameVisualizer(EventHandler):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        
        self.large_font = pygame.freetype.SysFont('Calibri', 150)
        self.medium_font = pygame.freetype.SysFont('Calibri', 50)
        self.small_font = pygame.freetype.SysFont('Calibri', 25)

        self.time_tracking = {
            0: [],
            1: []
        }
        self.count_down_start = 38*60
        self.start_time = 0
        self.current_team = 1
        self.current_state = 'No touch and no motion'
        
        self.state_machine_image = {}
        self.team_icon = {}
        self.load_images()

        self.snap_time = 0

    @staticmethod
    def format_seconds(total_seconds):
        t = floor(total_seconds)
        hours = (t // 3600)
        minutes = (t // 60) % 60
        seconds = t % 60

        return hours, minutes, seconds

    def load_images(self):
        self.state_machine_image['No touch and no motion'] = pygame.image.load('StateMachine/state_machine_no_touch_no_motion.gv.png')
        self.state_machine_image['Touch'] = pygame.image.load('./StateMachine/state_machine_touch.gv.png')
        self.state_machine_image['Motion and no touch'] = pygame.image.load('./StateMachine/state_machine_motion_no_touch.gv.png')
        self.state_machine_image['Touch and motion'] = pygame.image.load('./StateMachine/state_machine_touch_motion.gv.png')
        self.state_machine_image['Motion'] = pygame.image.load('./StateMachine/state_machine_motion.gv.png')
        self.state_machine_image['No motion'] = pygame.image.load('./StateMachine/state_machine_no_motion.gv.png')

        self.team_icon['red'] = pygame.image.load('CurlingStoneIconRed50px.png')

        self.team_icon['yellow'] = pygame.image.load('CurlingStoneIconYellow50px.png')
        self.team_icon['green'] = pygame.image.load('CurlingStoneIconGreen50px.png')
        self.team_icon['blue'] = pygame.image.load('CurlingStoneIconBlue50px.png')

        self.image_indicator_icon = pygame.image.load('CameraIcon.png').convert()

    def render_state_machine(self):
        self.screen.blit(self.state_machine_image[self.current_state], (50, 75))

    def render_motion_table(self):
        self.medium_font.render_to(self.screen, (600, 50), 'Motion table', (0, 0, 0))
        for index, (identifier, motion) in enumerate(self.motion_table.items()):
            x = index % 4
            y = index // 4
            color = '#7eeda5' if motion else 'white'
        
            pygame.draw.circle(self.screen, color, (600 + 150*x, 150 + 125*y), 50)
            pygame.gfxdraw.aacircle(self.screen, 600 + 150*x, 150 + 125*y, 50, (122, 122, 122))
            
            team = (identifier & 32) >> 5
            letter = chr(ord('A') + int((identifier & 24) >> 3))
            number = (identifier & 7) + 1
            self.small_font.render_to(self.screen, (582 + 150*x, 165 + 125*y), f'{letter}{number}', (0, 0, 0))
            if team:
                self.screen.blit(self.team_icon['blue'], (578 + 150*x, 115 + 125*y))
            else:
                self.screen.blit(self.team_icon['green'], (578 + 150*x, 115 + 125*y))

    def render_image_indicator(self):
        seconds = 2

        alpha = 255 - 255*(time() - self.snap_time)/seconds
        if alpha > 255:
            alpha = 255
        elif alpha < 0:
            alpha = 0

        self.image_indicator_icon.set_alpha(alpha)
        self.screen.blit(self.image_indicator_icon, (1350, 50))
        
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
            self.large_font.render_to(self.screen, (40 + 700*team, 700), f'{minutes:02.0f}:{seconds:02.0f}', color)
        self.render_state_machine()
        self.render_motion_table()
        self.render_image_indicator()
        
        self.medium_font.render_to(self.screen, (100, 625), 'Team Green')
        self.medium_font.render_to(self.screen, (800, 625), 'Team Blue')
        self.screen.blit(self.team_icon['green'], (40, 618))
        self.screen.blit(self.team_icon['blue'], (740, 618))
        self.small_font.render_to(self.screen, (100, 50), f'{self.current_state}', (0, 0, 0))

    def start_timer(self):
        self.time_tracking[self.current_team].append([time()])

        self.start_time = time()

    def stop_timer(self):
        if len(self.time_tracking[self.current_team]):
            self.time_tracking[self.current_team][-1].append(time())

            self.current_team = not self.current_team

    def no_touch_no_motion_event(self):
        if self.current_state != 'Touch' and self.current_state != 'Motion and no touch':
            self.start_timer()

        if self.current_state == 'Motion' or self.current_state == 'No motion':
            print('Take picture and update website')
            self.snap_time = time()
            takePicture()
        self.current_state = 'No touch and no motion'

    def motion_no_touch_event(self):
        self.current_state = 'Motion and no touch'

    def touch_event(self):
        self.current_state = 'Touch'

    def touch_motion_event(self):
        self.current_state = 'Touch and motion'

    def motion_event(self):
        self.current_state = 'Motion'
        self.stop_timer()

    def no_motion_event(self):
        self.current_state = 'No motion'
