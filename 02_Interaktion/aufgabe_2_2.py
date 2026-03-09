# import sys
# sys.path.append("..")
# sys.path.append(".")
# from FMLRobot import FMLRobot
# from FMLMqtt import FMLMqtt

# # MQTT broker configuration
# broker_address = "mqttbroker"
# topic = "groupX/color"

# # Initialize the MQTT client
# mqtt_client = FMLMqtt(broker_address, broker_port=1884, topic=topic)

# # Try to connect to the MQTT broker
# if mqtt_client.connect():
#     print("Connection successful! Proceeding with MQTT operations...")
    
#     # Publish a message to the topic
#     mqtt_client.publish("Hello from main script!")
    
#     # Wait for a message to be published and read it
#     print("Waiting for a message...")
#     received_message = mqtt_client.read_message()
#     print(f"Received message: {received_message}")
    
# else:
#     print("Failed to connect to MQTT broker. Exiting.")

# # Gracefully disconnect after receiving the message
# mqtt_client.disconnect()

# import sys
# sys.path.append("..")
# sys.path.append(".")

# from FMLRobot import FMLRobot
# from FMLMqtt import FMLMqtt
# import time

# broker_address = "mqttBroker"
# topic = "groupX/color"

# mqtt_client = FMLMqtt(broker_address, broker_port=1884, topic=topic)

# if mqtt_client.connect():
#     print("MQTT connected")

#     with FMLRobot() as robot:

#         while True:

#             print("Waiting for command...")
#             command = mqtt_client.read_message()

#             if command == "Detect color":

#                 # read color from sensor
#                 color = robot.get_color_left()

#                 print("Detected:", color)

#                 # publish detected color
#                 mqtt_client.publish(color)

#                 print("Waiting for confirmation...")

#                 confirmation = mqtt_client.read_message()

#                 if confirmation == "correctly recognized":
#                     print("Color confirmed correct")
#                     break

#                 else:
#                     print("Color incorrect, retrying...")

# else:
#     print("Failed to connect to MQTT broker")

# mqtt_client.disconnect()


import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLMqtt import FMLMqtt

# MQTT broker configuration
broker_address = "mqttbroker"
topic = "groupX/color"

# Initialize the MQTT client
mqtt_client = FMLMqtt(broker_address, broker_port=1884, topic=topic)

# Try to connect to the MQTT broker
if mqtt_client.connect():
    print("Connection successful! Proceeding with MQTT operations...")
    
    # Publish a message to the topic
    mqtt_client.publish("Hello from main script!")
    
    # Wait for a message to be published and read it
    print("Waiting for a message...")
    received_message = mqtt_client.read_message()
    print(f"Received message: {received_message}")
    
else:
    print("Failed to connect to MQTT broker. Exiting.")

# Gracefully disconnect after receiving the message
mqtt_client.disconnect()

import sys
sys.path.append("..")
sys.path.append(".")

from FMLRobot import FMLRobot
from FMLMqtt import FMLMqtt
import time

broker_address = "mqttBroker"
color_topic = "group5/color"
cmd_topic = "group5/cmd"

color_client = FMLMqtt(broker_address, broker_port=1884, topic=color_topic)
cmd_client = FMLMqtt(broker_address, broker_port=1884, topic=cmd_topic)

if color_client.connect() and cmd_client.connect():
    print("MQTT clients connected")

    with FMLRobot() as robot:

        while True:

            print("Waiting for command on topic group5/color...")
            command = color_client.read_message()

            if command == "Detect color":

                # read color from sensor
                color = robot.get_color_left()

                print("Detected:", color)

                # publish detected color to groupX/color
                color_client.publish(color)

                print("Waiting for confirmation on topic group5/cmd...")

                confirmation = cmd_client.read_message()

                if confirmation == "correctly recognized":
                    print("Color confirmed correct")
                    break

                else:
                    print("Color incorrect, retrying...")

else:
    print("Failed to connect to one or more MQTT brokers")

color_client.disconnect()
cmd_client.disconnect()