# Picklogger counter on polycomp signature board web server.
Here is a a web server on a Raspberry Pi Zero to control your Polycomp signage board via the RS232 port. Here's a step-by-step guide to get you started:

# 1. Gather the required materials:

Raspberry Pi Zero, 3, 4 (W or WH version with built-in Wi-Fi is preferred)
MicroSD card (8GB or larger) with Raspbian OS installed
Power supply for the Raspberry Pi
Polycomp signage board documentation (for understanding the RS232 commands)

# 2. Connect your Raspberry Pi:

Insert the microSD card into the Raspberry Pi Zero.
Connect any peripherals you need (e.g., a keyboard, mouse, display) for initial setup and configuration.
Power on the Raspberry Pi Zero.

# 3. Set up the Raspberry Pi:

Follow the initial setup prompts on the screen to configure your Raspberry Pi Zero with Raspbian OS. Ensure you have an active internet connection.

# 4. Enable SSH and Wi-Fi (if necessary):

To enable SSH, you can use the raspi-config tool by running the command: sudo raspi-config. Then, navigate to "Interfacing Options" and enable SSH.
If you're using a Raspberry Pi Zero W or WH and want to connect via Wi-Fi, also configure Wi-Fi through the raspi-config tool.

# 5. Update your Raspberry Pi:

Open a terminal on the Raspberry Pi or connect to it via SSH from another device.
Run the following commands to update the package list and upgrade existing packages:

```
sudo apt update
sudo apt upgrade
```

# 6. Install required software:

Install Python and Flask, which will be used to create the web server:

```
sudo apt install python3-pip
pip3 install Flask
```

# 7. Create the Flask web application:

Create a new directory for your web application and navigate to it:

```
mkdir polycomp
cd polycomp
```

Create a new Python file, e.g., app.py - use the app.py

# 8. Create the HTML template:

Create a new directory called templates:

```
mkdir templates
```
Create a new HTML file, e.g., index.html, inside the templates directory:

# 9. Run the web server:

Save the app.py and index.html files.
Start the Flask web server by running the following command inside the web_app directory:

```
python3 app.py
```

# 10. 10. Access the web server:

With the web server running, you can access it from any device on the same network by entering the Raspberry Pi's IP address in a web browser. For example, if your Raspberry Pi's IP address is 192.168.1.100, enter http://192.168.1.100 in the browser's address bar.

# Important Notes:

Make sure to properly handle exceptions and errors in your code, especially when dealing with external hardware like RS232 connections.
Ensure you understand the RS232 commands your Polycomp signage board expects and verify them before sending any commands.
By following these steps, you should have a basic web server running on your Raspberry Pi Zero that allows you to enter text and send commands to your Polycomp signage board via the RS232 port.

# additional info:

To resolve the "Permission denied" error, try the following steps:

1. Ensure correct permissions: Check if the user running the app.py script has the necessary permissions to access the serial port. You can do this by adding the user to the dialout group, which usually grants access to serial ports. Run the following command:

```
sudo usermod -a -G dialout YOUR_USERNAME
```


# Automatic start

set up your Flask app to run on startup so that it automatically starts when your Raspberry Pi boots up. To achieve this, you can use systemd, which is a system and service manager for Linux.

Here are the steps to configure your Flask app to run on startup using systemd:

# Step 1: Create a service file

Create a service file for your Flask app. Open a terminal and create a new file using a text editor (e.g., nano or vim).

```
sudo nano /etc/systemd/system/picklogger.service
```

Replace picklogger with a name of your choice. This will be the name of the service that you can use to start, stop, or restart your Flask app.

# Step 2: Add the following configuration to the service file

```
[Unit]
Description=Picklogger Counter App
After=network.target

[Service]
WorkingDirectory=/path/to/your/app
ExecStart=/usr/bin/python3 /path/to/your/app/app.py
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=picklogger
User=your_username

[Install]
WantedBy=multi-user.target
```

Replace /path/to/your/app with the full path to the directory where your app.py and other project files are located.

Replace your_username with your actual username (the user who has access to the serial port and the Flask app).

# Step 3: Save and close the file

For nano, press Ctrl+O to save the file and Ctrl+X to exit.

# Step 4: Reload systemd and enable the service

Run the following commands to reload the systemd daemon and enable your service to run on startup:

```
sudo systemctl daemon-reload
sudo systemctl enable picklogger.service
```

# Step 5: Start the service

To start the service and run your Flask app, use the following command:

```
sudo systemctl start picklogger.service
```

# Step 6: Verify status

You can check the status of the service to ensure it's running properly:

```
sudo systemctl status picklogger.service
```

If everything is set up correctly, your Flask app should now run on startup every time your Raspberry Pi boots up. It will be accessible at http://localhost:8080 (or whichever port you have configured). If you encounter any issues or need further assistance, please let me know, and I'll be glad to help!


