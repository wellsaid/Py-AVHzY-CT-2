#!/usr/bin/env python
from serial import Serial as Serial

from struct import unpack as unpack
from argparse import ArgumentParser as ArgumentParser
from argparse import FileType as FileType

from time import sleep as sleep

from sys import exit as exit

# actions along with their description
actions = [ "list", "read" ]
action_descriptions = {
    "list" : "Show this list and exit",
    "read" : "Reads energy value from the meter" }

first_exec = True
timestamp = 0

# ---------------------------------------------- ACTION HANDLERS ------------------------------------------- #
def action_list():
    print("Actions list:")
    for action in action_descriptions:
        print("  ", action, "\t", action_descriptions[action])

def action_read(ser, output):
    global first_exec
    global timestamp

    if first_exec:
        output.write("time,voltage,current,power,voltageDP,voltageDM\n")
        first_exec = False
    
    ser.write(b"Get Meter Data")

    voltage = unpack("f", ser.read(4))[0]
    current = unpack("f", ser.read(4))[0]
    power = unpack("f", ser.read(4))[0]
    voltageDP = unpack("f", ser.read(4))[0]
    voltageDM = unpack("f", ser.read(4))[0]

    output.write("{0},{1},{2},{3},{4},{5}\n".format(timestamp, voltage, current, power, voltageDP, voltageDM))
    
# action handlers in a dictionary
action_handlers = {
    "list" : action_list,
    "read" : action_read }
# ---------------------------------------------------------------------------------------------------------------------- #

def perform_action(device, action, repeat, time, output):
    global timestamp
    
    if action == "list":
        action_list()
        return
    
    # -------------------------------------- SERIAL PORT OPENING
    ser = Serial(device)
    # TODO:  Set Baud rate and stuff (needed? python defaults are working on my device)

    # -------------------------------------- ACTION LOOP
    count = 0
    while count != repeat:
        action_handlers[action](ser, output)
        if repeat != -1:
            count += 1
        if count != repeat:
            try:
                sleep(time)
            except KeyboardInterrupt:
                break
            timestamp += time

    ser.close();
    output.close();

def main():
    
    # -------------------------------------- OPTION PARSING
    parser = ArgumentParser(description="Program to interact with the AVHzY CT-2 power meter")
    parser.add_argument("action",
                        metavar="action", choices=actions,
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
    args = parser.parse_args()

    if args.repeat < -1:
        print("ERROR: repeat must be in >= -1")
        parser.print_usage()
        exit(1)

    if args.time < 0.02:
        print("ERROR: time must be >= 0.02")
        parser.print_usage()
        exit(1)

    perform_action(args.device, args.action, args.repeat, args.time, args.output)
    exit(0)

if __name__ == "__main__":
    main()
