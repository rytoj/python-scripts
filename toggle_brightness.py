# -*- coding: utf-8 -*-

import re
import subprocess


def run_command(command):
    """
    Run linux command
    :param command: list separated command
    :return: output and return code
    """
    return subprocess.call(command)


def turn_off_brightness(display_name):
    """
    Turns off display brightness
    :param display_name:
    :return:
    """
    command = "xrandr --output {DISPLAY_NAME} --brightness 0".format(DISPLAY_NAME=display_name)
    return run_command(command.split())


def turn_on_brightness(display_name):
    """
    Turns off display brightness
    :param display_name:
    :return:
    """
    command = "xrandr --output {DISPLAY_NAME} --brightness 1".format(DISPLAY_NAME=display_name)
    return run_command(command.split())


def list_all_displays():
    command = "xrandr --verbose "
    return subprocess.check_output(command.split()).decode()


def get_displays(xrandr_output):
    """
    Get list of connected displays
    :param xrandr_output: xranr --verbose output
    :return: monitor name and brightness value
    [('HDMI-0 ', '1'), ('DVI-1 ', '1')]
    """
    displays = []
    brightness = []
    regex = "[a-zA-Z]*-\d.* connected"
    brightness_regex = "Brightness: [0-9].[0-9]"

    matches = re.finditer(regex, xrandr_output)
    for match in matches:
        displays.append(match.group().split(" connected")[0])

    matches = re.finditer(brightness_regex, xrandr_output)
    for match in matches:
        brightness.append(match.group().split(": ")[1][0])

    return dict(zip(displays, brightness))


def _run_as_standalone_script():
    """Runs program as standalone script."""
    # return_code = turn_on_brightness("HDMI-0")
    xrand_verbose_output = list_all_displays()
    displays_dict = get_displays(xrand_verbose_output)
    import sys
    try:
        passed_argument = sys.argv[1]
        brightness_value = displays_dict[passed_argument]
        if brightness_value == "1":
            turn_off_brightness(passed_argument)
        if brightness_value == "0":
            turn_on_brightness(passed_argument)


    except (KeyError, IndexError):
        print("Incorrect display name\n")
        print("Available options: \n{}".format(displays_dict))
        print("\nUsage:\n{} 'DISPLAY_NAME'".format(sys.argv[0]))


if __name__ == '__main__':
    _run_as_standalone_script()
