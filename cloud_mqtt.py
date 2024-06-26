from umqtt.simple import MQTTClient
import time
from machine import UART, Pin
from time import sleep
import ustruct
import ujson
# MQTT broker settings
with open('config.json', 'r') as file:
    json_string = file.read()
config = ujson.loads(json_string)

print("Configuration loaded from config.json")
print(config)
MQTT_BROKER= config["MQTT_BROKER"]
MQTT_PORT = config["MQTT_PORT"]
MQTT_v1= config["MQTT_v1"]
MQTT_v2 = config["MQTT_v2"]
MQTT_v3 = config["MQTT_v3"]
MQTT_i1= config["MQTT_i1"]
MQTT_i2 = config["MQTT_i2"]
MQTT_i3 = config["MQTT_i3"]
MQTT_CLIENT_ID = config["MQTT_CLIENT_ID"]
SSID = config["SSID"]
PASSWORD = config["PASSWORD"]
Tx=config["tx"]
Rx=config["rx"]
BAUDRATE=config["Baudrate"]
# MQTT client settings
Timeout=config["timeout"]
control=config["Control"]
ct = Pin(control, Pin.OUT)
uart = UART(1, baudrate=BAUDRATE, tx=Pin(Tx), rx=Pin(Rx) )#timeout=Timeout)

# Function to calculate CRC16
def calculate_crc16(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

request = bytearray([0x02, 0x03,0x00,0x00,0x00,0x28])

crc = calculate_crc16(request)
request.append(crc & 0xFF)
request.append((crc >> 8) & 0xFF)
reading_quantity=request[5]
array_size=(reading_quantity*2)+7
buffer = bytearray(array_size)
print(request)

def connect_wifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print('WiFi connected:', wlan.ifconfig())

def connect_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    return client

def main():
    connect_wifi()
    client = connect_mqtt()
    
    while True:
        try:
            
            while True:
                print("#########################################################")
                ct.value(1)
                uart.write(request)
                uart.flush()
                ct.value(0)
                bytes_read = uart.readinto(buffer)
                
                if bytes_read:
                    response = buffer[:bytes_read]
                    a= [hex(b) for b in response]
                    print(a)
                    
                    if len(response) >= 9:
                        received_crc = (response[-2] << 8) | response[-3]
                        expected_crc = calculate_crc16(response[1:-3])
                        if received_crc == expected_crc:
                            print (a)
                            
#                             client.publish(MQTT_TOPIC, str(a))
                            print("CRC check passed")
                            slave_address = response[1]
                            function_code = response[2]
                            byte_count = response[3]
                            register_values = response[4:-3]
                            print("Slave Address:", slave_address)
                            print("Function Code:", function_code)
                            print("Byte Count:", byte_count)
                            print("Register Values:", [hex(val) for val in register_values])
                            v1_reg1 = register_values[0]
                            v1_reg2 = register_values[1]
                            v1_reg3 = register_values[2]
                            v1_reg4 = register_values[3]
                            v2_reg1= register_values[4]
                            v2_reg2= register_values[5]
                            v2_reg3 = register_values[6]
                            v2_reg4 = register_values[7]
                            v3_reg1 = register_values[8]
                            v3_reg2 = register_values[9]
                            v3_reg3 = register_values[10]
                            v3_reg4 = register_values[11]
                            i1_reg1= register_values[-12]
                            i1_reg2 = register_values[-11]
                            i1_reg3= register_values[-10]
                            i1_reg4 = register_values[-9]
                            i2_reg1= register_values[-8]
                            i2_reg2= register_values[-7]
                            i2_reg3= register_values[-6]
                            i2_reg4= register_values[-5]
                            i3_reg1= register_values[-4]
                            i3_reg2= register_values[-3]
                            i3_reg3= register_values[-2]
                            i3_reg4= register_values[-1]
                            combined_value = (v1_reg1 << 24) | (v1_reg2 << 16) | (v1_reg3 << 8) | v1_reg4
                            print("Type:",type(combined_value))
                            print("Combined Value:", hex(combined_value))
                            combined_bytes = bytearray(4)
                            combined_bytes[0] = combined_value & 0xFF
                            combined_bytes[1] = (combined_value >> 8) & 0xFF
                            combined_bytes[2] = (combined_value >> 16) & 0xFF
                            combined_bytes[3] = (combined_value >> 24) & 0xFF

                            combined_bytes = ustruct.pack('>I', combined_value)
                            float_value = ustruct.unpack('>f', combined_bytes)[0]

                            print( float_value)
                            combined_value1 = (v2_reg1 << 24) | (v2_reg2 << 16) | (v2_reg3 << 8) | v2_reg4
                            print("Combined Value1:", hex(combined_value1))
                            combined_bytes1 = bytearray(4)
                            combined_bytes1[0] = combined_value1 & 0xFF
                            combined_bytes1[1] = (combined_value1 >> 8) & 0xFF
                            combined_bytes1[2] = (combined_value1 >> 16) & 0xFF
                            combined_bytes1[3] = (combined_value1 >> 24) & 0xFF

                            combined_bytes1 = ustruct.pack('>I', combined_value1)
                            float_value1 = ustruct.unpack('>f', combined_bytes1)[0]

                            print( float_value1)
                            combined_value2 = (v3_reg1 << 24) | (v3_reg2 << 16) | (v3_reg3 << 8) | v3_reg4
                            print("Combined Value:", hex(combined_value2))
                            combined_bytes2 = bytearray(4)
                            combined_bytes2[0] = combined_value2 & 0xFF
                            combined_bytes2[1] = (combined_value2 >> 8) & 0xFF
                            combined_bytes2[2] = (combined_value2 >> 16) & 0xFF
                            combined_bytes2[3] = (combined_value2 >> 24) & 0xFF

                            combined_bytes2 = ustruct.pack('>I', combined_value2)
                            float_value2 = ustruct.unpack('>f', combined_bytes2)[0]

                            print( float_value2)
                            combined_value3 = (i1_reg1 << 24) | (i1_reg2 << 16) | (i1_reg3 << 8) | i1_reg4
                            print("Combined Value:", hex(combined_value3))
                            combined_bytes3 = bytearray(4)
                            combined_bytes3[0] = combined_value3 & 0xFF
                            combined_bytes3[1] = (combined_value3 >> 8) & 0xFF
                            combined_bytes3[2] = (combined_value3 >> 16) & 0xFF
                            combined_bytes3[3] = (combined_value3 >> 24) & 0xFF

                            combined_bytes3 = ustruct.pack('>I', combined_value3)
                            float_value3= ustruct.unpack('>f', combined_bytes3)[0]

                            print( float_value3)
                            combined_value4 = (i2_reg1 << 24) | (i2_reg2 << 16) | (i2_reg3 << 8) | i2_reg4
                            print("Combined Value:", hex(combined_value4))
                            combined_bytes4 = bytearray(4)
                            combined_bytes4[0] = combined_value4 & 0xFF
                            combined_bytes4[1] = (combined_value4 >> 8) & 0xFF
                            combined_bytes4[2] = (combined_value4 >> 16) & 0xFF
                            combined_bytes4[3] = (combined_value4 >> 24) & 0xFF

                            combined_bytes4 = ustruct.pack('>I', combined_value4)
                            float_value4 = ustruct.unpack('>f', combined_bytes4)[0]

                            print( float_value4)
                            combined_value5 = (i3_reg1 << 24) | (i3_reg2 << 16) | (i3_reg3 << 8) | i3_reg4
                            print("Combined Value:", hex(combined_value5))
                            combined_bytes5 = bytearray(4)
                            combined_bytes5[0] = combined_value5 & 0xFF
                            combined_bytes5[1] = (combined_value5 >> 8) & 0xFF
                            combined_bytes5[2] = (combined_value5 >> 16) & 0xFF
                            combined_bytes5[3] = (combined_value5 >> 24) & 0xFF

                            combined_bytes5 = ustruct.pack('>I', combined_value5)
                            float_value5 = ustruct.unpack('>f', combined_bytes5)[0]

                            print( float_value5)


                            print()
                            client.publish(MQTT_v1, str(float_value))
                            client.publish(MQTT_v2,str(float_value1))
                            client.publish(MQTT_v3,str(float_value2))
                            client.publish(MQTT_i1,str(float_value3))
                            client.publish(MQTT_i2,str(float_value4))
                            client.publish(MQTT_i3,str(float_value5))
                        else:
                              pass
                    else:
                        print("Received incomplete response")
                else:
                    print("No data recived")
                    print("------------------------------------------------------------------")
                sleep(5) 

        except OSError as e:
            print('Error:', e)
            client = connect_mqtt()  # Reconnect to MQTT broker

if __name__ == '__main__':
    main()


