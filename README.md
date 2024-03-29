# Introduction 
Sheep often go missing while grazing in *communal fields*. Locating missing livestock is tedious and time consuming.

We prototype a virtual fencing solution to prevent sheep to escape from a field. Our goals are to:

- Reduce the number of sheep lost
- Reduce cost for farmers
- Ensure safety for sheep
- Create a solution that is durable and easily repairable
- Maintain job security for shepherd's

# Code Usage
## Receiver
receiver.py is ran on the receiver, or Arduino Nano rp2040 board, using CircuitPython. secrets.py is also needed on the board. It should be renamed code.py
## Transmitter
transmitter.py is ran on the transmitter, or Raspberry Py Pico board, using MicroPython. It should be renamed code.py .
Note that it also requires the two libraries, httpParser.py and esp8266.py, which were modified from [this link](https://circuitdigest.com/microcontroller-projects/interfacing-esp8266-01-wifi-module-with-raspberry-pi-pico). Further functionalities can be added to the code using [this link](https://room-15.github.io/blog/2015/03/26/esp8266-at-command-reference/).
### Steps to use run the code on the transmitter
1. Install [Thonny](https://thonny.org/)
2. Install [Micropython](https://micropython.org/download/rp2-pico/) on pico (bootsel, download the file and put it on the board, and it will restart on its own)
Note: the pico board won't show up any more on the computer, and its normal. The files are still accessible with Thonny.
3. Connect pico board to computer and start thonny
Note: to save stuff to the board, make sure that no other editor has the pico files open (e.g. mu editor)
4. Click bottom right corner and select micropython
Note: there might be multiple micropythons, select the one for which, when you save a file, allows you to save it on the pico board.
5. Create new file, name it esp8266.py, copy inside the contents of esp8266.py and save it to the pico board
6. repeat for httpParser.py
7. Open new file, put code.py and run with green button


