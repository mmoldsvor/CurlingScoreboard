from time import sleep
from serial import Serial
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo
from serial.serialutil import SerialException

from typing import Optional


def process_value(state: bytes):
    if len(state):
        value = int.from_bytes(state, byteorder='little')

        touch = value & 1
        motion = (value & 2) >> 1
        identifier = (value & ~3) >> 2

        print(f'0b{value:08b}')
        print(f'Id: {identifier}, Touch: {touch}, Motion:{motion}')


def connect_to_device(port: ListPortInfo):
    with serial.Serial(port.device) as serial_device:
        print(f'Connected to {serial_device.name}')
        while True:        
            process_value(serial_device.read())


def main(ble_serial_number: Optional[str]  = '000000000000'):
    while True:
        try:
            port, = (port for port in comports() if port.serial_number == ble_serial_number)
            print(type(port))
            connect_to_device(port)
        except SerialException as e:
            print(f'Lost connection to device {port.device}.')
        except ValueError as e:
            print(f'No device found with serial number {ble_serial_number}.')
        print('Trying to connect...')
        sleep(5)


if __name__ == '__main__':
    main()