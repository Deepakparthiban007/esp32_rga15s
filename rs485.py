from umqtt.simple import MQTTClient
import time
from machine import UART, Pin
from time import sleep
import ustruct
# MQTT broker settings
MQTT_BROKER = '192.168.1.145'  # Replace with your MQTT broker's IP address
MQTT_PORT = 1883 # Replace with your MQTT broker's port
MQTT_TOPIC = '/voltage1'# MQTT topic as a byte string
MQTT_TOPIC1 =  '/voltage2'
MQTT_TOPIC2 = '/voltage3'
MQTT_TOPIC3 = '/current1'
MQTT_TOPIC4 = '/current2'
MQTT_TOPIC5  = '/current3'
    

# WiFi settings
SSID = 'RadioStudioACT'
PASSWORD = 'rastu2014'

# MQTT client settings
MQTT_CLIENT_ID = 'test@1234321'

ct = Pin(4, Pin.OUT)
uart = UART(1, 9600, tx=Pin(17), rx=Pin(16), timeout=75)

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
                            a = register_values[0]
                            b = register_values[1]
                            c = register_values[2]
                            d = register_values[3]
                            e = register_values[4]
                            f = register_values[5]
                            g = register_values[6]
                            h = register_values[7]
                            i = register_values[8]
                            j = register_values[9]
                            k = register_values[10]
                            l = register_values[11]
                            m = register_values[-12]
                            n = register_values[-11]
                            o= register_values[-10]
                            p = register_values[-9]
                            q= register_values[-8]
                            r= register_values[-7]
                            s= register_values[-6]
                            t= register_values[-5]
                            u= register_values[-4]
                            v= register_values[-3]
                            w= register_values[-2]
                            x= register_values[-1]
                            combined_value = (a << 24) | (b << 16) | (c << 8) | d
                            print("Combined Value:", hex(combined_value))
                            combined_bytes = bytearray(4)
                            combined_bytes[0] = combined_value & 0xFF
                            combined_bytes[1] = (combined_value >> 8) & 0xFF
                            combined_bytes[2] = (combined_value >> 16) & 0xFF
                            combined_bytes[3] = (combined_value >> 24) & 0xFF

                            combined_bytes = ustruct.pack('>I', combined_value)
                            float_value = ustruct.unpack('>f', combined_bytes)[0]

                            print( float_value)
                            combined_value1 = (e << 24) | (f << 16) | (g << 8) | h
                            print("Combined Value1:", hex(combined_value1))
                            combined_bytes1 = bytearray(4)
                            combined_bytes1[0] = combined_value1 & 0xFF
                            combined_bytes1[1] = (combined_value1 >> 8) & 0xFF
                            combined_bytes1[2] = (combined_value1 >> 16) & 0xFF
                            combined_bytes1[3] = (combined_value1 >> 24) & 0xFF

                            combined_bytes1 = ustruct.pack('>I', combined_value1)
                            float_value1 = ustruct.unpack('>f', combined_bytes1)[0]

                            print( float_value1)
                            combined_value2 = (i << 24) | (j << 16) | (k << 8) | l
                            print("Combined Value:", hex(combined_value2))
                            combined_bytes2 = bytearray(4)
                            combined_bytes2[0] = combined_value2 & 0xFF
                            combined_bytes2[1] = (combined_value2 >> 8) & 0xFF
                            combined_bytes2[2] = (combined_value2 >> 16) & 0xFF
                            combined_bytes2[3] = (combined_value2 >> 24) & 0xFF

                            combined_bytes2 = ustruct.pack('>I', combined_value2)
                            float_value2 = ustruct.unpack('>f', combined_bytes2)[0]

                            print( float_value2)
                            combined_value3 = (m << 24) | (n << 16) | (o << 8) | p
                            print("Combined Value:", hex(combined_value3))
                            combined_bytes3 = bytearray(4)
                            combined_bytes3[0] = combined_value3 & 0xFF
                            combined_bytes3[1] = (combined_value3 >> 8) & 0xFF
                            combined_bytes3[2] = (combined_value3 >> 16) & 0xFF
                            combined_bytes3[3] = (combined_value3 >> 24) & 0xFF

                            combined_bytes3 = ustruct.pack('>I', combined_value3)
                            float_value3= ustruct.unpack('>f', combined_bytes3)[0]

                            print( float_value3)
                            combined_value4 = (q << 24) | (r << 16) | (s << 8) | t
                            print("Combined Value:", hex(combined_value4))
                            combined_bytes4 = bytearray(4)
                            combined_bytes4[0] = combined_value4 & 0xFF
                            combined_bytes4[1] = (combined_value4 >> 8) & 0xFF
                            combined_bytes4[2] = (combined_value4 >> 16) & 0xFF
                            combined_bytes4[3] = (combined_value4 >> 24) & 0xFF

                            combined_bytes4 = ustruct.pack('>I', combined_value4)
                            float_value4 = ustruct.unpack('>f', combined_bytes4)[0]

                            print( float_value4)
                            combined_value5 = (u << 24) | (v << 16) | (w << 8) | x
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
                            client.publish(MQTT_TOPIC, str(float_value))
                            client.publish(MQTT_TOPIC1,str(float_value1))
                            client.publish(MQTT_TOPIC2,str(float_value2))
                            client.publish(MQTT_TOPIC3,str(float_value3))
                            client.publish(MQTT_TOPIC4,str(float_value4))
                            client.publish(MQTT_TOPIC5,str(float_value5))
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


