from serial import Serial


def process_value(bytes):
    value = int.from_bytes(bytes, byteorder='little')

    touch = value & 1
    motion = (value & 2) >> 1
    identifier = (value & ~3) >> 2

    print(f'0b{value:08b}')
    print(f'Id: {identifier}, Touch: {touch}, Motion:{motion}')


def main():
    with Serial('COM11') as ser:
        print(f'Connected to {ser.name}')
        while True:        
            process_value(ser.read())


if __name__ == '__main__':
    main()