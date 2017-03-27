#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import sys

HOSTNAME = "8.8.8.8"
SOUNDUP = os.getcwd() + '/static/up.wav'
SOUNDDOWN = os.getcwd() + '/static/down.wav'
command_uplink = 'mplayer %s 1>/dev/null 2>&1' % SOUNDUP
command_downlink = 'mplayer %s 1>/dev/null 2>&1' % SOUNDDOWN


def sleep(seconds):
    return time.sleep(seconds)


def ping(count, host=HOSTNAME, interval=1):
    countd = 0  # Count downtime
    try:
        count = int(count)
        if count:
            pass
        while count > 0:
            response = os.system("ping -q -c 1 " + host + " 1>/dev/null")
            if response == 0:
                print host, 'is up!'
                if countd > 15:
                    os.system(command_uplink)  # Link up sound
                countd = 0
            else:
                print host, 'is down! counter: {}'.format(countd)
            count -= 1
            countd += 1
            if countd % 60 == 0:
                print command_downlink
                os.system(command_downlink)  # Link down sound
            sleep(interval)
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except KeyboardInterrupt as e:
        print("\nInterrupted by keyboard")


def main():
    ping(1000000000000)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
        sys.exit()

    if len(sys.argv) != 3:
        print 'Usage: %s host delay-time' % sys.argv[0]
    else:
        print(sys.argv)
        ping(count=sys.argv[1], host=sys.argv[2])
