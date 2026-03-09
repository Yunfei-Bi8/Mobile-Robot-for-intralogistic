import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLMqtt import FMLMqtt
import time

mqtt = FMLMqtt(broker_address="mqttBroker", topic="group5/hubgeruest",broker_port=1884)
if mqtt.connect():
    print("MQTT clients connected")
else :print("fail to connect")
with FMLRobot() as robot:
    print("Robot ready. Waiting for MQTT commands ('up' or 'down') on topic 'group5/hubgeruest'...")
    
    # try:
        # 3. Continuous loop to listen for messages
    while True:
            # read_message() blocks until a new message arrives
            command = mqtt.read_message() 
            # print(f"Received command: {command}")
            
            # 4. Control the fork and send feedback via MQTT
            if command == "up":
                print("Lifting fork...")
                robot.lift_fork()
                mqtt.publish("Feedback: Fork successfully raised to transport height.")
                
            elif command == "down":
                print("Dropping fork...")
                robot.drop_fork()
                mqtt.publish("Feedback: Fork successfully lowered to the ground.")
                
            else:
                # Handle incorrect keywords
                mqtt.publish(f"Error: Unknown command '{command}'. Please use 'up' or 'down'.")
                
    # except KeyboardInterrupt:
    #     # Allows you to stop the script gracefully using Ctrl+C
    #     print("\nStopping script...")

# Disconnect from broker when exiting
mqtt.disconnect()
