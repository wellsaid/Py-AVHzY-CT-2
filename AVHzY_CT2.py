#!/usr/bin/env python
from serial import Serial as Serial

from struct import unpack as unpack
from argparse import ArgumentParser as ArgumentParser
from argparse import FileType as FileType

from time import sleep as sleep

from sys import exit as exit

# actions along with their description
__actions = [ "list", "read" ]
__action_descriptions = {
        "list" : "Show this list and exit",
        "read" : "Reads energy value from the meter" }

# values for read operation
__gets = [ "all", "voltage", "current", "power", "voltageDP", "voltageDM", "energy" ]

class AVHzY_CT2:

    def __init__(self, device, action, repeat, time, reads, output):
        self.__action = action
        self.__repeat = repeat
        self.__time = time
        self.__output = output
        self.__ser = Serial(device)

        self.__first_exec = True
        self.__timestamp = 0
        self.__energy = 0
        self.__prev_timestamp = 0

        if reads == "all":
            self.__reads = [ "voltage", "current", "power", "voltageDP", "voltageDM", "energy" ]
        else:
            self.__reads = reads

        # action handlers in a dictionary
        self.__action_handlers = {
            "list" : self.__action_list,
            "read" : self.__action_read }

    def __del__(self):
            self.__ser.close();
            self.__output.close();

    def __action_list(self):
        print("Actions list:")
        for action in __action_descriptions:
            print("  ", action, "\t", __action_descriptions[action])

    def __action_read(self):

        if self.__first_exec:
            self.__output.write("time");
            for r in self.__reads:
                self.__output.write(",{0}".format(r))
            self.__output.write("\n")
            self.__first_exec = False
            
        self.__ser.write(b"Get Meter Data")

        sleep(0.02)
        
        voltage = unpack("f", self.__ser.read(4))[0]
        current = unpack("f", self.__ser.read(4))[0]
        power = unpack("f", self.__ser.read(4))[0]
        voltageDP = unpack("f", self.__ser.read(4))[0]
        voltageDM = unpack("f", self.__ser.read(4))[0]

        self.__output.write("{0}".format(self.__timestamp))
        if "voltage" in self.__reads:
            self.__output.write(",{0}".format(voltage))
        if "current" in self.__reads:
            self.__output.write(",{0}".format(current))
        if "power" in self.__reads:
            self.__output.write(",{0}".format(power))
        if "voltageDP" in self.__reads:
            self.__output.write(",{0}".format(voltageDP))
        if "voltageDM" in self.__reads:
            self.__output.write(",{0}".format(voltageDM))
        if "energy" in self.__reads:
            if self.__timestamp == 0:
                self.__output.write(",0")
            else:
                self.__energy += ((self.__timestamp - self.__prev_timestamp)*power)/3600
                self.__output.write(",{0}".format(self.__energy))
        self.__output.write("\n")
        self.__output.flush()
        
    def perform_action(self):
        if self.__action == "list":
            self.__action_list()
            return
        
        count = 0
        while count != self.__repeat:

            self.__action_handlers[self.__action]()

            try:
                sleep(self.__time - 0.02)
            except KeyboardInterrupt:
                break

            self.__prev_timestamp = self.__timestamp
            self.__timestamp += self.__time

            if self.__repeat != -1:
                count += 1

    def change_output(self, output):
        self.__output.close()
        self.__output = output
                                    
def main():
    
    # -------------------------------------- OPTION PARSING
    parser = ArgumentParser(description="Program to interact with the AVHzY CT-2 power meter")
    parser.add_argument("action",
                        metavar="action", choices=__actions,
                        help="The action to perform [choices: %(choices)s]")
    parser.add_argument("-d", "--device",
                        default="/dev/ttyACM0",
                        help="Path to the device [default: %(default)s]")
    parser.add_argument("-r", "--repeat",
                        type=int, default=-1,
                        help="How many times to repeat the operation. Must be in [-1, inf[ (-1: infinite) [default: %(default)s]")
    parser.add_argument("-t", "--time",
                        type=float, default=2,
                        help="The time (in seconds) to wait between each action iteration. Must be in [0.02, inf[ [default: %(default)s]")
    parser.add_argument("-o", "--output",
                        default="-", type=FileType('w'),
                        help="Where to write output of the action [default: stdout]")
    parser.add_argument("-g", "--get",
                        default="all", choices=__gets, nargs="+",
                        help="For read operation: what to get from power meter [choices: %(choices)s default: %(default)s")
    args = parser.parse_args()

    if args.repeat < -1:
        print("ERROR: repeat must be in >= -1")
        parser.print_usage()
        exit(1)

    if args.time < 0.02:
        print("ERROR: time must be >= 0.02")
        parser.print_usage()
        exit(1)

    AVHzY_CT2(args.device, args.action, args.repeat, args.time, args.get, args.output).perform_action()
    exit(0)

if __name__ == "__main__":
    main()
