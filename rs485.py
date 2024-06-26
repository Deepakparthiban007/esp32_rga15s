from machine import UART, Pin
import time

uart = UART(1, baudrate=9600, tx=17, rx=16, timeout=1000) 

DE_PIN= 4
de_pin = Pin(DE_PIN,Pin.OUT)

#SLAVE_ID = 02

def toggle_de_pin(state):
    de_pin.value(state)

def send_modbus_frame(data):
    toggle_de_pin(1)  
    uart.write(data)
    toggle_de_pin(0)  

def receive_modbus_frame():
    toggle_de_pin(0)  
    frame = uart.read()
    toggle_de_pin(1) 
    return frame


def read_holding():
    request = bytearray([0x02, 0x03, 0xEC, 0x00, 0x00, 0x01,0x84,0x39])  
    send_modbus_frame(request)
    time.sleep(0.01)  
    response = receive_modbus_frame()
    return response
response = read_holding()
print("Response:", response) 



