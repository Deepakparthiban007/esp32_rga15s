from machine import UART, Pin
from time import sleep

# Setup control pin
ct = Pin(4, Pin.OUT)

# Initialize UART
uart = UART(1, 9600, tx=Pin(17), rx=Pin(16), timeout=100)

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

request = bytearray([0x02, 0x03, 0xEC, 0x00, 0x00, 0x02])
crc = calculate_crc16(request)
request.append(crc & 0xFF)
request.append((crc >> 8) & 0xFF)
buffer = bytearray(9)
while True:
    # Set control pin to transmit mode
    ct.value(1)
    

    uart.flush()
    # Send the request
    uart.write(request)
    uart.flush()
#      sleep(5)  # Short delay to ensure transmission is complete
    
    # Set control pin to receive mode
    ct.value(0)
    
    # Prepare buffer to read response (9 bytes for this example)
#     buffer = bytearray(9)
    
    # Read into the buffer
    bytes_read = uart.readinto(buffer)
    print("no.of bytes received: ",bytes_read)
    
    if bytes_read:
        # Slice the buffer to the actual size of the read data
        response = buffer[:bytes_read]
        
        # Print received raw data
        print("Received raw data:", [hex(b) for b in response])
        
        # Check if response length is at least 5 (minimum length of a valid response)
        if len(response) >= 9:
            # Extract and verify CRC
            received_crc = (response[-1] << 8) | response[-2]
            expected_crc = calculate_crc16(response[:-2])
            
            if received_crc == expected_crc:
                print("CRC check passed")
                # Process response (example: decode register values)
                slave_address = response[0]
                function_code = response[1]
                byte_count = response[2]
                register_values = response[3:-2]
                
                # Print decoded response
                print("Slave Address:", slave_address)
                print("Function Code:", function_code)
                print("Byte Count:", byte_count)
                print("Register Values:", [hex(val) for val in register_values])
            else:
                print("CRC check failed")
                print(f"Expected CRC: {hex(expected_crc)}, Received CRC: {hex(received_crc)}")
        else:
            print("Received incomplete response")
    else:
        print("No data recived")
    sleep(2)  # Delay before the next iteration
 
 
  

