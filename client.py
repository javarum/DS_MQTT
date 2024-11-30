import logging
import time
import random
from datetime import datetime
from paho.mqtt import client as mqtt_client

BROKER = "emqx"
PORT = 1883
REGISTER_TOPIC = "factory/machines/register"
SENSOR_TOPIC = "factory/machines/sensor_data"
SHUTDOWN_TOPIC = "factory/machines/shutdown"
CLIENT_ID = "client-1"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

is_registered = False

def on_connect(client, userdata, flags, rc, properties=None):
    """Handle connection to the MQTT broker."""
    global is_registered
    if rc == 0:
        logging.info("Connected successfully to MQTT broker.")
        client.subscribe(SHUTDOWN_TOPIC)
        if register_machine(client, CLIENT_ID):
            is_registered = True
    else:
        logging.error(f"Failed to connect with return code {rc}")



def on_disconnect(client, userdata, rc):
    """Handle disconnection from the MQTT broker."""
    logging.warning(f"Disconnected with result code: {rc}")


def on_message(client, userdata, msg):
    """Handle incoming messages."""
    logging.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    if msg.topic == SHUTDOWN_TOPIC:
        shutdown_message = msg.payload.decode()
        if "critical" in shutdown_message.lower():
            logging.warning("Critical shutdown command received. Shutting down machine.")
            exit(1)


def connect_mqtt():
    """Initialize and connect the MQTT client."""
    client = mqtt_client.Client(client_id=CLIENT_ID, protocol=mqtt_client.MQTTv5)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect_async(BROKER, PORT)
    return client


def register_machine(client, machine_id):
    """Register the machine with a unique ID."""
    message = f"Machine {machine_id} registered."
    result = client.publish(REGISTER_TOPIC, message)
    if result[0] == 0:
        logging.info(f"Machine registered: {machine_id}")
        return True
    else:
        logging.error(f"Failed to register machine {machine_id}")
        return False


def publish_sensor_data(client, machine_id):
    """Publish sensor data with a timestamp."""
    global is_registered
    while True:
        if not is_registered:
            logging.warning("Machine not registered yet. Waiting to publish sensor data...")
            time.sleep(2)
            continue

        timestamp = datetime.utcnow().isoformat()
        vibration = random.uniform(0.5, 1.5)
        temperature = random.uniform(20.0, 100.0)
        error_code = random.choice(["OK", "WARN", "ERROR"])

        message = {
            "timestamp": timestamp,
            "machine_id": machine_id,
            "vibration": vibration,
            "temperature": temperature,
            "error_code": error_code
        }
        result = client.publish(SENSOR_TOPIC, str(message))
        if result[0] == 0:
            logging.info(f"Published sensor data: {message}")
        else:
            logging.error(f"Failed to publish sensor data")

        if error_code == "ERROR":
            logging.error("Critical error detected. Shutting down machine.")
            exit(1)

        time.sleep(5)


def run():
    """Run the MQTT client."""
    client = connect_mqtt()
    client.loop_start()

    try:
        publish_sensor_data(client, CLIENT_ID)
    except KeyboardInterrupt:
        logging.info("Graceful shutdown")
    finally:
        client.loop_stop()


if __name__ == "__main__":
    run()
