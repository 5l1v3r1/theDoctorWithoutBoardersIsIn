from subprocess import Popen, PIPE
from time import sleep
from operator import itemgetter

addresses = {}

def setup():
    commands = []
    commands.append("ifconfig wlan0 down")
    commands.append("iwconfig wlan0 mode monitor")
    commands.append("ifconfig wlan0 up")
    for command in commands:
        process = Popen(command.split(), stdout=PIPE)
        output = process.communicate()[0]
        sleep(.5)
        print command, output

def teardown():
    commands = []
    commands.append("ifconfig wlan0 down")
    commands.append("iwconfig wlan0 mode managed")
    commands.append("ifconfig wlan0 up")
    for command in commands:
        process = Popen(command.split(), stdout=PIPE)
        output = process.communicate()[0]
        sleep(.5)
        print command, output


def capture():
    command = "tcpdump -e -i wlan0 -n"
    process = Popen(command.split(), stdout=PIPE)
    output = iter(process.stdout.readline, "")
    for line in output:
        packet = line.split()
        address = ''
        db = 0
        for info in packet:
            if "SA" in info:
                address = info[3:]
            if "dB" in info:
                db = int(info.split("dB")[0])
        addresses[address] = db
        sorted_DBs = sorted(addresses.items(), key=itemgetter(1))
        print sorted_DBs[len(sorted_DBs) - 10:]


    
def main():
    setup()
    capture()

import atexit
atexit.register(teardown)

main()


