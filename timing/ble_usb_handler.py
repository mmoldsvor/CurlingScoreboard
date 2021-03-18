from time import sleep

from threading import Thread

from serial import Serial
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo
from serial.serialutil import SerialException
from queue import Queue

from typing import Optional


class CommunicationThread:
    def __init__(self, ble_serial_number: Optional[str]  = '000000000000'):
        self.ble_serial_number = ble_serial_number
        self.queue = Queue()
        
        thread = Thread(target=self.run, daemon=True)
        thread.start()

    def process_value(self, state: bytes):
        if len(state):
            value = int.from_bytes(state, byteorder='little')
            
            self.queue.put(value)      

    def connect_to_device(self, port: ListPortInfo):
        with Serial(port.device) as serial_device:
            print(f'Connected to {serial_device.name}')
            while True:        
                self.process_value(serial_device.read())
                
    def run(self):
        while True:
            try:
                port, = (port for port in comports() if port.serial_number == self.ble_serial_number)
                self.connect_to_device(port)
            except SerialException:
                print(f'Lost connection to device {port.device}.')
            except ValueError:
                print(f'No device found with serial number {self.ble_serial_number}.')
            print('Trying to connect...')
            sleep(5)
