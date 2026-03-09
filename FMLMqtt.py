import paho.mqtt.client as mqtt
import threading

class FMLMqtt:
    def __init__(self, broker_address, broker_port=1884, topic="test/topic"):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.topic = topic
        self.client = mqtt.Client()
        self.last_message = None  # To store the last received message
        self.message_event = threading.Event()  # Event to signal when a message is received
        self.connection_event = threading.Event()  # Event to signal when the connection is successful
        self.is_connected = False  # To store the connection status

        # Bind the callback methods
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """Callback when the client connects to the broker."""
        if rc == 0:
            print("Connected to MQTT broker")
            self.is_connected = True  # Connection successful
            self.client.subscribe(self.topic)  # Subscribe to the topic after connecting
        else:
            print(f"Connection failed with result code {rc}")
            self.is_connected = False  # Connection failed

        self.connection_event.set()  # Signal that the connection attempt is complete

    def on_message(self, client, userdata, message):
        """Callback when a message is received."""
        decoded_message = message.payload.decode()
        print(f"Message received on topic {message.topic}")
        self.last_message = decoded_message  # Store the last received message
        self.message_event.set()  # Signal that a message has been received

    def connect(self):
        """Connect to the MQTT broker and return True if successful."""
        self.connection_event.clear()  # Reset the event before connection attempt
        self.client.connect(self.broker_address, self.broker_port, keepalive=60)
        self.client.loop_start()

        # Wait for the connection to complete (or fail)
        self.connection_event.wait()  # Block until on_connect signals completion

        return self.is_connected  # Return the connection status (True/False)

    def publish(self, message):
        """Publish a message to the default topic."""
        self.client.publish(self.topic, message)

    def subscribe(self, topic=None):
        """Subscribe to a new topic. If no topic is provided, subscribe to the default topic."""
        if topic:
            self.topic = topic
        self.client.subscribe(self.topic)
        print(f"Subscribed to topic: {self.topic}")

    def disconnect(self):
        """Disconnect from the broker."""
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT broker")

    def read_message(self):
        """Wait until a message is published and return it."""
        self.message_event.wait()  # Block until a message is received
        message = self.last_message
        self.message_event.clear()  # Clear the event for the next message
        return message
