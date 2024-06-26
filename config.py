import ujson

config = {
    "MQTT_BROKER": "192.168.1.145",
    "MQTT_PORT": 1883,
    "MQTT_v1": "/v1",
    "MQTT_v2": "/v2",
    "MQTT_v3": "/v3",
    "MQTT_i1": "/i1",
    "MQTT_i2": "/i2",
    "MQTT_i3": "/i3",
    "MQTT_CLIENT_ID": "test@1234321",
    "SSID" : "RadioStudioACT",
    "PASSWORD" :"rastu2014",
    "Baudrate" : 9600,
    "tx" : 17,
    "rx" : 16,
    "timeout" : 75,
    "Control" : 4
    
}

json_string = ujson.dumps(config)

with open('config.json', 'w') as file:
    file.write(json_string)

