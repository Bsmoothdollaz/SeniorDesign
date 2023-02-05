import serial

ser = serial.Serial()

ser.port = 'COM3'
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.stopbits = serial.STOPBITS_ONE
ser.parity = serial.PARITY_NONE
ser.timeout = 0.2

ser.open()

while True:
    msg = input(' *** enter a command ***')

    if msg.upper() == 'Q':
        break

    msg += ';'

    ser.write(msg.encode('utf-8'))
    recv = ser.readall()
    print(recv.decode('utf-8'))

ser.close()