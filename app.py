# app.py
from flask import Flask, render_template, jsonify, request
import json
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIO Pin Configuration
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO_PINS = {
    "1": 17,  # GPIO pin for Living Room Light
    "2": 27,  # GPIO pin for Kitchen Light
    "3": 22   # GPIO pin for Bedroom Fan
}

# Initialize GPIO pins
for pin in GPIO_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Start with all appliances off

# Load appliance states from a JSON file
def load_appliances():
    with open('appliances.json') as f:
        return json.load(f)

# Save appliance states to a JSON file
def save_appliances(data):
    with open('appliances.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    appliances = load_appliances()
    return render_template('index.html', appliances=appliances)

@app.route('/toggle', methods=['POST'])
def toggle_appliance():
    appliance_id = request.json['id']
    appliances = load_appliances()

    # Toggle appliance status
    appliances[appliance_id]["status"] = not appliances[appliance_id]["status"]
    
    # Control GPIO pin based on new appliance status
    pin = GPIO_PINS[appliance_id]
    GPIO.output(pin, GPIO.HIGH if appliances[appliance_id]["status"] else GPIO.LOW)
    
    # Save updated data
    save_appliances(appliances)
    return jsonify(appliances[appliance_id])

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()  # Ensure GPIO pins are reset when the app stops

