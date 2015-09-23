# ultraborg-web
Web based interface for controlling UltraBorg from a phone or browser.
![](screenshot.png?raw=true)

This example provides web-based access to an UltraBorg using a web browser on both phones and desktops.
This allows you to both read ultrasonic distances and move servos via a Raspberry Pi.

[You can find out more about UltraBorg here](https://www.piborg.org/ultraborg)

## Getting ready
Before using this script you should make sure your UltraBorg is working with the standard examples.
We would also suggest you tune the servos using the Tuning GUI, but this is entirely optional.

Make sure your Raspberry Pi is connected to your router before running the scripts.
This example should work with both WiFi and Ethernet based connections.

## Downloading the code
To get the code we will clone this repository to the Raspberry Pi.
In a terminal run the following commands
```bash
cd ~
git clone https://github.com/piborg/ultraborg-web.git
```

## Running the code
This is easiest done via SSH over the network.

First find out what your IP address is using the `ifconfig` command.
It should be 4 numbers separated by dots, e.g. `192.168.0.198`
We will need this to access the controls, so make a note of it.

Next run the main script on your Raspberry Pi using sudo:
`sudo ~/ultraborg-web/ubWeb.py`

Wait for the script to load, when it is ready it should say:
`Press CTRL+C to terminate the web-server`

## Controlling your servos
Load your web browser on your phone or desktop.
Once loaded enter your IP address in the address bar

You should be presented with sliders for each servo, some current servo position readings, and some distance readings.
![](screenshot.png?raw=true)

To move a servo simply tap or click on the new position you want.
You can also drag the slider up and down, the servo should move whilst you are dragging it. 

The values at the bottom are the distance readings in mm.
A value of *None* indicates either:
* There is no ultrasonic module attached to that connector
* The distance you are measuring is extremely close, within a couple of centimeters
* The distance you are measuring is too far away, more than a few meters
* If changing between *None* and a value the ultrasonic module is struggling to "see" the object

## Alternative options
There are some other URLs you can use to get different functionality.
Replace `192.168.0.198` in the below addresses with your IP address:
* http://192.168.0.198 - Standard controls, allows servo control and reads distances
* http://192.168.0.198/servo - Servo controls only, no distances are displayed
* http://192.168.0.198/distances - Gets the distance readings without the servo controls, refreshes at a regular intervale
* http://192.168.0.198/distances-once - Single set of distance readings, you may need to force-refresh to get new values

## Additional settings
There are some settings towards the top of the script which may be changed to adjust the behaviour of the interface:
* `webPort` - Sets the port number, 80 is the default port web browsers will try
* `displayRate` - The number of times per second the web browser will refresh the distance readings
* `sliderHeight` - The height of the sliders in pixels, adjust this if the sliders are too tall or too short

## Auto start at boot
To get the web interface to load on its own do the following:

1. Open the Cron table using `crontab -e`
2. Add a cron job to the bottom of the file:
   `@reboot /home/pi/ultraborg-web/ubWeb.py`
3. Save the file
4. Close the file

The cron table should now auto-run the script when the Raspberry Pi boots up.

## Going further
This is just a simple example of how a web interface can be made using Python on the Raspberry Pi to control a servos are read sensors.

We think sharing software is awesome, so we encourage others to extend and/or improve on this script to make it do even more :)
