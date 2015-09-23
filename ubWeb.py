#!/usr/bin/env python
# coding: Latin-1

# Creates a web-page interface for UltraBorg

# Import library functions we need
import UltraBorg
import time
import sys
import threading
import SocketServer

# Settings for the web-page
webPort = 80                            # Port number for the web-page, 80 is what web-pages normally use
displayRate = 2                         # Number of times to read the ultrasonic readings per second
sliderHeight = 800                      # The number of pixels high to make the sliders

# Setup the UltraBorg
global UB
UB = UltraBorg.UltraBorg()              # Create a new UltraBorg object
UB.Init()                               # Set the board up (checks the board is connected)

# Class used to implement the web server
class WebServer(SocketServer.BaseRequestHandler):
    def handle(self):
        global UB
        # Get the HTTP request data
        reqData = self.request.recv(1024).strip()
        reqData = reqData.split('\n')
        # Get the URL requested
        getPath = ''
        for line in reqData:
            if line.startswith('GET'):
                parts = line.split(' ')
                getPath = parts[1]
                break
        if getPath.startswith('/distances-once'):
            # Ultrasonic distance readings
            # Get the readings
            distance1 = int(UB.GetDistance1())
            distance2 = int(UB.GetDistance2())
            distance3 = int(UB.GetDistance3())
            distance4 = int(UB.GetDistance4())
            # Build a table for the values
            httpText = '<html><body><table border="0" style="width:100%%"><tr>'
            if distance1 == 0:
                httpText += '<td width="25%%"><center><h2>None</h2></center></td>'
            else:
                httpText += '<td width="25%%"><center><h2>%04d</h2></center></td>' % (distance1)
            if distance2 == 0:
                httpText += '<td width="25%%"><center><h2>None</h2></center></td>'
            else:
                httpText += '<td width="25%%"><center><h2>%04d</h2></center></td>' % (distance2)
            if distance3 == 0:
                httpText += '<td width="25%%"><center><h2>None</h2></center></td>'
            else:
                httpText += '<td width="25%%"><center><h2>%04d</h2></center></td>' % (distance3)
            if distance4 == 0:
                httpText += '<td width="25%%"><center><h2>None</h2></center></td>'
            else:
                httpText += '<td width="25%%"><center><h2>%04d</h2></center></td>' % (distance4)
            httpText += '</tr></table></body></html>'
            self.send(httpText)
        elif getPath.startswith('/set/'):
            # Servo position setting: /set/servo/position
            parts = getPath.split('/')
            # Get the power levels
            if len(parts) >= 4:
                try:
                    servo = int(parts[2])
                    position = float(parts[3])
                except:
                    # Bad values
                    servo = 0
                    position = 0.0
            else:
                # Bad request
                servo = 0
                position = 0.0
            # Ensure settings are within limits
            if position < -1:
                position = -1
            elif position > 1:
                position = 1
            # Set the new servo position
            if servo == 1:
                UB.SetServoPosition1(position)
            elif servo == 2:
                UB.SetServoPosition2(position)
            elif servo == 3:
                UB.SetServoPosition3(position)
            elif servo == 4:
                UB.SetServoPosition4(position)
            # Read the current servo positions
            position1 = UB.GetServoPosition1() * 100.0
            position2 = UB.GetServoPosition2() * 100.0
            position3 = UB.GetServoPosition3() * 100.0
            position4 = UB.GetServoPosition4() * 100.0
            # Build a table for the values
            httpText = '<html><body><table border="0" style="width:100%%"><tr>'
            httpText += '<td width="25%%"><center><h2>%.0f %%</h2></center></td>' % (position1)
            httpText += '<td width="25%%"><center><h2>%.0f %%</h2></center></td>' % (position2)
            httpText += '<td width="25%%"><center><h2>%.0f %%</h2></center></td>' % (position3)
            httpText += '<td width="25%%"><center><h2>%.0f %%</h2></center></td>' % (position4)
            httpText += '</tr></table></body></html>'
            self.send(httpText)
        elif getPath == '/':
            # Main page, move sliders to change the servo positions
            httpText = '<html>\n'
            httpText += '<head>\n'
            httpText += '<style>\n'
            httpText += ' input[type=range][orient=vertical]\n'
            httpText += ' {\n'
            httpText += '  writing-mode: bt-lr; /* IE */\n'
            httpText += '  -webkit-appearance: slider-vertical; /* WebKit */\n'
            httpText += '  padding: 0 0;\n'
            httpText += ' }\n'
            httpText += '</style>\n'
            httpText += '<script language="JavaScript"><!--\n'
            httpText += 'function SetServo(servo, position) {\n'
            httpText += ' var iframe = document.getElementById("setPosition");\n'
            httpText += ' position = position / 100.0;\n'
            httpText += ' iframe.src = "/set/" + servo + "/" + position;\n'
            httpText += '}\n'
            httpText += '//--></script>\n'
            httpText += '</head>\n'
            httpText += '<body>\n'
            httpText += '<table border="0" style="width:100%%;"><tr>'
            httpText += ' <td width="25%%"><center>'
            httpText += '  <input type="range" min="-100" max="100" value="0" orient="vertical" style="width:100%%; height:%dpx" onchange="SetServo(1, this.value);" />\n' % (sliderHeight)
            httpText += ' </center></td>'
            httpText += ' <td width="25%%"><center>'
            httpText += '  <input type="range" min="-100" max="100" value="0" orient="vertical" style="width:100%%; height:%dpx" onchange="SetServo(2, this.value);" />\n' % (sliderHeight)
            httpText += ' </center></td>'
            httpText += ' <td width="25%%"><center>'
            httpText += '  <input type="range" min="-100" max="100" value="0" orient="vertical" style="width:100%%; height:%dpx" onchange="SetServo(3, this.value);" />\n' % (sliderHeight)
            httpText += ' </center></td>'
            httpText += ' <td width="25%%"><center>'
            httpText += '  <input type="range" min="-100" max="100" value="0" orient="vertical" style="width:100%%; height:%dpx" onchange="SetServo(4, this.value);" />\n' % (sliderHeight)
            httpText += ' </center></td>'
            httpText += '</tr></table>'
            httpText += '<iframe id="setPosition" src="/set/0/0" width="100%%" height="100" frameborder="0"></iframe>\n'
            httpText += '<br /><center><h2>Distances (mm)</h2></centre><br />\n'
            httpText += '<iframe src="/distances" width="100%%" height="100" frameborder="0"></iframe>\n'
            httpText += '</body>\n'
            httpText += '</html>\n'
            self.send(httpText)
        elif getPath == '/servo':
            # Alternative page with only servo control, move sliders to change the servo positions
            httpText = '<html>\n'
            httpText += '<head>\n'
            httpText += '<style>\n'
            httpText += ' input[type=range][orient=vertical]\n'
            httpText += ' {\n'
            httpText += '  writing-mode: bt-lr; /* IE */\n'
            httpText += '  -webkit-appearance: slider-vertical; /* WebKit */\n'
            httpText += '  padding: 0 0;\n'
            httpText += ' }\n'
            httpText += '</style>\n'
            httpText += '<script language="JavaScript"><!--\n'
            httpText += 'function SetServo(servo, position) {\n'
            httpText += ' var iframe = document.getElementById("setPosition");\n'
            httpText += ' position = position / 100.0;\n'
            httpText += ' iframe.src = "/set/" + servo + "/" + position;\n'
            httpText += '}\n'
            httpText += '//--></script>\n'
            httpText += '</head>\n'
            httpText += '<body>\n'
            httpText += '<table border="0" style="width:100%%;"><tr>'
            httpText += ' <td width="25%%"><center>'
            httpText += '  <input type="range" min="-100" max="100" value="0" orient="vertical" style="width:100%%; height:%dpx" onchange="SetServo(1, this.value);" />\n' % (sliderHeight)
            httpText += ' </center></td>'
            httpText += ' <td width="25%%"><center>'
            httpText += '  <input type="range" min="-100" max="100" value="0" orient="vertical" style="width:100%%; height:%dpx" onchange="SetServo(2, this.value);" />\n' % (sliderHeight)
            httpText += ' </center></td>'
            httpText += ' <td width="25%%"><center>'
            httpText += '  <input type="range" min="-100" max="100" value="0" orient="vertical" style="width:100%%; height:%dpx" onchange="SetServo(3, this.value);" />\n' % (sliderHeight)
            httpText += ' </center></td>'
            httpText += ' <td width="25%%"><center>'
            httpText += '  <input type="range" min="-100" max="100" value="0" orient="vertical" style="width:100%%; height:%dpx" onchange="SetServo(4, this.value);" />\n' % (sliderHeight)
            httpText += ' </center></td>'
            httpText += '</tr></table>'
            httpText += '<iframe id="setPosition" src="/set/0/0" width="100%%" height="100" frameborder="0"></iframe>\n'
            httpText += '</body>\n'
            httpText += '</html>\n'
            self.send(httpText)
        elif getPath == '/distances':
            # Repeated reading of the ultrasonic distances, set a delayed refresh
            # We use AJAX to avoid screen refreshes caused by refreshing a frame
            displayDelay = int(1000 / displayRate)
            httpText = '<html>\n'
            httpText += '<head>\n'
            httpText += '<script language="JavaScript"><!--\n'
            httpText += 'function readDistances() {\n'
            httpText += ' var xmlhttp;\n'
            httpText += ' if (window.XMLHttpRequest) {\n'
            httpText += '  // code for IE7+, Firefox, Chrome, Opera, Safari\n'
            httpText += '  xmlhttp = new XMLHttpRequest();\n'
            httpText += ' } else {\n'
            httpText += '  // code for IE6, IE5\n'
            httpText += '  xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");\n'
            httpText += ' }\n'
            httpText += ' xmlhttp.onreadystatechange = function() {\n'
            httpText += '  var div = document.getElementById("readDistances");\n'
            httpText += '  var DONE = 4;\n'
            httpText += '  var OK = 200;\n'
            httpText += '  if (xmlhttp.readyState == DONE) {\n'
            httpText += '   if (xmlhttp.status == OK) {\n'
            httpText += '    div.innerHTML = xmlhttp.responseText;\n'
            httpText += '   } else {\n'
            httpText += '    div.innerHTML = "<center><h2>Failed reading distances (not running?)</h2></center>";\n'
            httpText += '   }\n'
            httpText += '  }\n'
            httpText += ' }\n'
            httpText += ' xmlhttp.open("GET","distances-once",true);\n'
            httpText += ' xmlhttp.send();\n'
            httpText += ' setTimeout("readDistances()", %d);\n' % (displayDelay)
            httpText += '}\n'
            httpText += '//--></script>\n'
            httpText += '</head>\n'
            httpText += '<body>\n'
            httpText += '<body onLoad="setTimeout(\'readDistances()\', %d)">\n' % (displayDelay)
            httpText += '<div id="readDistances"><center><h2>Waiting for first distance reading...</h2></center></div>\n'
            httpText += '</body>\n'
            httpText += '</html>\n'
            self.send(httpText)
        else:
            # Unexpected page
            self.send('Path : "%s"' % (getPath))

    def send(self, content):
        self.request.sendall('HTTP/1.0 200 OK\n\n%s' % (content))

# Run the web server until we are told to close
httpServer = SocketServer.TCPServer(("0.0.0.0", webPort), WebServer)
try:
    print 'Press CTRL+C to terminate the web-server'
    while True:
        httpServer.handle_request()
except KeyboardInterrupt:
    # CTRL+C exit
    print '\nUser shutdown'

print 'Web-server terminated.'
