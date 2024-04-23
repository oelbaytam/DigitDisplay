from DigitDisplay import SegmentDisplay

segments = [11,4,23,8,7,10,18,25]
digits = [22,27,17,24]

display = SegmentDisplay(segments, digits)

USERMENU = """
\033[1;36;40m Enter menu items to configure display:
\033[1;31;40m Press CTRL+C at anytime to exit the program.
"""

try:
    print(USERMENU)
    while True:
        entry = input("\033[1;33;40m Enter a 4 digit value:\033[1;37;40m")
        display.setValue(entry)
except KeyboardInterrupt:
    print("\033[1;37;40m")
    display.cleanup()
