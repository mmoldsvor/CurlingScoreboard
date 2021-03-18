from enum import Enum
from time import time

from event_handler import EventHandler

from typing import List

class State(Enum):
    NO_TOUCH_NO_MOTION = 1
    TOUCH = 2
    MOTION_NO_TOUCH = 3
    TOUCH_MOTION = 4
    MOTION = 5
    NO_MOTION = 6


class StateMachine:
    def __init__(self, current_state = State.NO_TOUCH_NO_MOTION, event_handlers: List[EventHandler] = None):
        self.current_stone = 0
        self.current_state = current_state
        self.event_handlers = event_handlers if not None else []
        self.motion_table = {} 
        self.motion_list = []
        
    def run(self, item):
        motion = (item & 2) >> 1
        identifier = (item & ~3) >> 2
        if identifier in self.motion_table:
            self.update_motion_table(identifier, motion)

        if self.current_state == State.NO_TOUCH_NO_MOTION:
            self.no_touch_no_motion_state(item)

        elif self.current_state == State.TOUCH:
            self.touch_state(item)

        elif self.current_state == State.MOTION_NO_TOUCH:
            self.motion_no_touch_state(item)

        elif self.current_state == State.TOUCH_MOTION:
            self.touch_motion_state(item)

        elif self.current_state == State.MOTION:
            self.motion_state(item)

        elif self.current_state == State.NO_MOTION:
            self.no_motion_state(item)

    def update_motion_table(self, identifier, motion):
        if identifier not in self.motion_list:
            self.motion_list.append(identifier)

        self.motion_table[identifier] = motion
        self.propagate_motion_table()

    def remove_motion_table(self, identifier):
        self.motion_table.pop(identifier)
        self.motion_list.remove(identifier)

        self.propagate_motion_table()

    def propagate_motion_table(self):
        for event_handler in self.event_handlers:
            event_handler.motion_table_update(self.motion_table)

    def propagate_events(self):
        for event_handler in self.event_handlers:
            if self.current_state == State.NO_TOUCH_NO_MOTION:
                event_handler.no_touch_no_motion_event()
            if self.current_state == State.TOUCH:
                event_handler.touch_event()
            if self.current_state == State.MOTION_NO_TOUCH:
                event_handler.motion_no_touch_event()
            if self.current_state == State.TOUCH_MOTION:
                event_handler.touch_motion_event()
            if self.current_state == State.MOTION:
                event_handler.motion_event()
            if self.current_state == State.NO_MOTION:
                event_handler.no_motion_event()

    def check_id(self, identifier):
        return self.current_stone == identifier
        
    def no_touch_no_motion_state(self, item):
        touch = item & 1
        motion = (item & 2) >> 1
        identifier = (item & ~3) >> 2

        if touch and identifier not in self.motion_table.keys():
            self.current_stone = identifier
            self.current_state = State.TOUCH
            self.propagate_events()
            
            self.update_motion_table(identifier, motion)

            self.touch_state(item)

        if motion and identifier not in self.motion_table.keys():
            self.current_stone = identifier
            self.current_state = State.MOTION_NO_TOUCH
            self.propagate_events()

            self.motion_no_touch_state(item)

    def touch_state(self, item):
        touch = item & 1
        motion = (item & 2) >> 1
        identifier = (item & ~3) >> 2

        if self.check_id(identifier) and not touch:
            self.current_state = State.NO_TOUCH_NO_MOTION
            self.remove_motion_table(identifier)
            self.propagate_events()

        elif self.check_id(identifier) and motion:
            self.current_state = State.TOUCH_MOTION
            self.propagate_events()

            self.touch_motion_state(item)

    def motion_no_touch_state(self, item):
        touch = item & 1
        motion = (item & 2) >> 1
        identifier = (item & ~3) >> 2

        if self.check_id(identifier) and not motion:
            self.current_state = State.NO_TOUCH_NO_MOTION
            self.propagate_events()

        elif self.check_id(identifier) and touch:
            self.current_state = State.TOUCH_MOTION
            self.propagate_events()

            self.update_motion_table(identifier, motion)

            self.touch_motion_state(item)

    def touch_motion_state(self, item):
        touch = item & 1
        identifier = (item & ~3) >> 2

        if self.check_id(identifier) and not touch:
            self.current_state = State.MOTION
            
            self.propagate_events()
            self.motion_state(item)

    def motion_state(self, item):
        motion = (item & 2) >> 1
        identifier = (item & ~3) >> 2

        if self.check_id(identifier) and not motion:
            self.current_state = State.NO_MOTION
            self.propagate_events()
            
            self.no_motion_state(item)

    def no_motion_state(self, item):
        if not sum(self.motion_table.values()):
            self.current_state = State.NO_TOUCH_NO_MOTION
            
            self.propagate_events()
