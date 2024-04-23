# A Class to work with the SH5461AS Segment Display using RPI GPIO pins
# Author: oelbaytam
# Last updated: 06-04-2024 

import RPi.GPIO as GPIO
import time, threading

class SegmentDisplay:
    NUM = {
    ' ':[0,0,0,0,0,0,0],
    '0':[1,1,1,1,1,1,0],
    '1':[0,1,1,0,0,0,0],
    '2':[1,1,0,1,1,0,1],
    '3':[1,1,1,1,0,0,1],
    '4':[0,1,1,0,0,1,1],
    '5':[1,0,1,1,0,1,1],
    '6':[1,0,1,1,1,1,1],
    '7':[1,1,1,0,0,0,0],
    '8':[1,1,1,1,1,1,1],
    '9':[1,1,1,1,0,1,1]} # preset pinouts for number values
    pins = None          # variable to hold pins corresponding to GPIO pins
    refreshThread = None # variable to hold refresh thread
    pinouts = [[0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]] # pinout variable, blank by default
    refreshing = False

    # Pins are used in BCM configuration.
    # Segments should be provided such that GIPO pins correspond to segment pins in order (11, 7, 4, 2, 1, 10, 5, 3)
    # Digits should be provided such that the GPIO pins correspond to digit pins in order (12, 9, 8, 6)
    def __init__(self, segments = [11,4,23,8,7,10,18,25], digits = [22, 27, 17, 24], starting_value=0):
        GPIO.setmode(GPIO.BCM)
        self.pins = digits
        self.pins += segments # add digits and segments to inordered array of GPIO output pins.
        GPIO.setup(self.pins, GPIO.OUT)
        self.setValue(starting_value)
        self.refreshThread = threading.Thread(target=self.changeDisplay)
        self.refreshing = True
        self.refreshThread.start()

    # Sets the value of the display 
    def setValue(self, value):
        self.pinouts = self.getPinOuts(str(value))

    # Gets digits and periods to the input string until there is no more digits, fills with blanks.
    def getPinOuts(self, strin):
        outputlist = [[0, 1, 1, 1],
                      [1, 0, 1, 1],
                      [1, 1, 0, 1],
                      [1, 1, 1, 0]]
        decimal = False
        currentdigit = 3
        # start at digit position 4 and loop through the inputted string.
        for char in strin[::-1]:
            # if the string is a digit, append that digit.
            if str.isdigit(char):
                outputlist[currentdigit] += self.NUM[char]
                #if the decimal flag is raised, append a decimal.
                if decimal:
                    outputlist[currentdigit].append(1)
                else:
                    outputlist[currentdigit].append(0)
                # go down a digit.
                currentdigit -= 1
            # if the character is a decimal, raise the decimal flag.
            if char == '.':
                decimal = True
            else:
                decimal = False
            # for extra digits fill with blanks.
        while currentdigit >= 0:
            outputlist[currentdigit] += [0, 0, 0, 0, 0, 0, 0, 0]
            currentdigit -= 1
        return outputlist

    # Always repeating function in the self.refreshThread to switch GPIO pins and display values on the display.
    def changeDisplay(self):
        while self.refreshing:
            pinouts = self.pinouts
            for pinset in pinouts:
                for i in range(4, 12):
                    GPIO.output(self.pins[i], pinset[i])
                GPIO.output(self.pins[0:4], pinset[0:4])
                time.sleep(0.005)

    # Cleans up the class at the end of the program.
    def cleanup(self):
        self.refreshing = False
        self.refreshThread.join()
        GPIO.cleanup()
