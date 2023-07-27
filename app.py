from flask import Flask, render_template, request

import serial

app = Flask(__name__, static_url_path='/static')

# Data variable to store the sent data
sent_data = ""

# Set up the serial connection
ser = serial.Serial('/dev/ttyS0', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

# Calculate the XOR checksum for the given data
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

# Convert text to hexadecimal representation with data modifiers
def text_to_hex_with_modifiers(text, color="default", flashing=False):
    color_modifiers = {
        "default": 0x44,
        "red": 0x52,
        "green": 0x47,
        "yellow": 0x59,
        "blue": 0x42,
        "pink": 0x50,
        "cyan": 0x43,
        "white": 0x57,
        "multi-color": 0x4D
    }
    color_modifier = color_modifiers[color.lower()] if color.lower() in color_modifiers else color_modifiers["default"]

    hex_data = ""

    if color != "default":
        hex_data += f"{0x1C:02X}{color_modifier:02X}"  # Add the color modifier if color is selected

 #   if flashing:
 #       hex_data += f"{0x1C:02X}46"  # Add the flashing modifier if selected

    for char in text:
        hex_data += f"{ord(char):02X}"

    return hex_data


# Send data over RS232 using the provided protocol
def send_data(hex_data, address=0):
    # Convert address to byte
    address_byte = bytes([address])

    # Prepare the data with EOT for checksum calculation
    data_with_eot = bytes.fromhex(f"00 53 {address:02X} 03 {hex_data} 04")

    # Calculate the checksum
    checksum = calculate_checksum(data_with_eot)

    # Prepare the full data to send (including headers and checksum)
    full_data = data_with_eot + bytes([checksum])

    # Send the data over RS232
    ser.write(full_data)

    # Create and return the complete HEX string
    hex_string = " ".join(hex(byte)[2:].zfill(2).upper() for byte in full_data)
    return hex_string


# Endpoint to handle form submission and send data to the server
@app.route("/", methods=["GET", "POST"])
def index():
    global sent_data

    if request.method == "POST":
        text = request.form["text"]
        color = request.form["color"]
        flashing = bool(request.form.get("flashing"))

        hex_data = text_to_hex_with_modifiers(text, color=color, flashing=flashing)
        hex_string = send_data(hex_data, address=1)

        # Update the sent_data variable with the complete HEX string
        sent_data = hex_string

    return render_template("index.html", data=sent_data)

# Endpoint to fetch the sent data from the server
@app.route("/get_sent_data", methods=["GET"])
def get_sent_data():
    global sent_data
    return sent_data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
