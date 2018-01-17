# -*- coding: utf-8 -*-
import unittest

from toggle_brightness import get_displays
from toggle_brightness import list_all_displays

xrand_test_data = """
Screen 0: minimum 320 x 200, current 4920 x 1920, maximum 8192 x 8192
eDP-1 connected primary 1920x1080+0+840 (0x4c) normal (normal left inverted right x axis y axis) 344mm x 194mm
	Identifier: 0x42
	Timestamp:  2218532
	Subpixel:   unknown
	Gamma:      1.0:1.0:1.0
	Brightness: 1.0
	Clones:    
	CRTC:       0


DP-1-3 connected 1080x1920+1920+0 (0x72) left (normal left inverted right x axis y axis) 477mm x 268mm
	Identifier: 0x4a
	Timestamp:  2218532
	Subpixel:   unknown
	Gamma:      1.0:1.0:1.0
	Brightness: 1.0
	Clones:    
	CRTC:       2

"""


class TestBrightness(unittest.TestCase):
    def test_get_display(self):
        self.assertEqual(get_displays(xrandr_output=xrand_test_data), {'eDP-1': '1', 'DP-1-3': '1'})

    def test_get_display_localy(self):
        xrand_verbose_output = list_all_displays()
        self.assertEqual(get_displays(xrandr_output=xrand_verbose_output), {'HDMI-0': '1', 'DVI-1': '1'})
