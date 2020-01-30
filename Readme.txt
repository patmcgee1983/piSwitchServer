This program is meant to control digital (on/off) devices connected to th PI on GPIO outputs. You connect to the PI through a web interface running on the client web browser.



Client:

Contains an html file. This file is to be opened on the client computer connecting to the raspberry PI.
You will need to enter the IP address of the PI you are connecting to in order to download the switch information.

You interact with the server via web requests and by receiving JSON data.

Server (PI):

The server is the raspberry pi. The pi should be connected to GPIO's to control.
You will need to know the IP address of the PI to connect to it.
There are two scripts which will be running, webServer.py and worker.py. WebServer.py serves out the web requests to the client and worker constantly checks the mySql database to see if any outputs need to be turned on or off.
