from enum import Enum
from time import time

from ble_usb_handler import CommunicationThread

class State(Enum):
    NO_TOUCH_MOTION = 1
    TOUCH = 2
    TOUCH_MOTION = 3
    MOTION = 4
    NO_MOTION = 5

class StateMachine:
    def __init__(self, current_state = State.NO_TOUCH_MOTION):
        self.current_stone = 0
        self.current_state = current_state
        self.motion_or_not = {} 
        
    def run(self, item):
        if self.current_state == State.NO_TOUCH_MOTION:
            self.no_touch_motion_state(item)

        elif self.current_state == State.TOUCH:
            self.touch_state(item)

        elif self.current_state == State.TOUCH_MOTION:
            self.touch_motion_state(item)

        elif self.current_state == State.MOTION:
            self.motion_state(item)

        elif self.current_state == State.NO_MOTION:
            self.no_motion_state(item)

        motion = (item & 2) >> 1
        identifier = (item & ~3) >> 2
        if identifier in self.motion_or_not and not self.check_id(identifier):
            self.motion_or_not[identifier] = motion

    def check_id(self, identifier):
        return self.current_stone == identifier
        
    def no_touch_motion_state(self, item):
        touch = item & 1
        identifier = (item & ~3) >> 2

        if touch or identifier in self.motion_or_not:
            self.motion_or_not[identifier] = 0

        if touch:
            self.current_stone = identifier
            self.current_state = State.TOUCH
            print('TOUCH')

    def touch_state(self, item):
        motion = (item & 2) >> 1
        identifier = (item & ~3) >> 2

        if self.check_id(identifier) and motion:
            self.current_state = State.TOUCH_MOTION
            print('TOUCH MOTION')

    def touch_motion_state(self, item):
        touch = item & 1
        identifier = (item & ~3) >> 2

        if self.check_id(identifier) and not touch:
            self.current_state = State.MOTION
            print('MOTION')

    def motion_state(self, item):
        motion = (item & 2) >> 1
        identifier = (item & ~3) >> 2

        if self.check_id(identifier) and not motion:
            self.current_state = State.NO_MOTION
            print('NO MOTION')
            self.no_motion_state(item)

    def no_motion_state(self, item):
        

        if not sum(self.motion_or_not.values()):
            self.current_state = State.NO_TOUCH_MOTION
            print('NO TOUCH MOTION\n')

if __name__ == '__main__':
    communication_thread = CommunicationThread()
    state_machine = StateMachine()
    while True:
        if not communication_thread.queue.empty():
            item = communication_thread.queue.get_nowait()

            state_machine.run(item)

            
            touch = item & 1
            motion = (item & 2) >> 1
            identifier = (item & ~3) >> 2
            #print(f'Touch: {touch}, Motion: {motion}, Identifier: {identifier}')
