#!/usr/bin/python
import appindicator
import logging
import gtk
import pyudev
import webcolors
import subprocess
import argparse
import os
import yaml
import sys

PRISM_HID_ID = '0003:00001038:00001225'
CONFIG_FILE_NAME = '.prism.config'

logger = logging.getLogger("Prism")


def eval(command):
    return subprocess.Popen(command, shell=True, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read().decode()


def reload():
    set_led_color(Config.read().color, False)


def find_device_path():
    context = pyudev.Context()
    for device in context.list_devices(HID_ID=PRISM_HID_ID):
        if device.sequence_number == 0:
            children = list(device.children)
            if children:
                child = children[0]
                if child.subsystem == 'hidraw':
                    return child['DEVNAME']

    raise ValueError("Couldn't detect any SteelSeries Elite Prism sound card")


def prompt_for_led_color():
    dialog = gtk.ColorSelectionDialog('SteelSeries Elite Prism color picker')
    colorselect = dialog.colorsel
    current_color = Config.read().color
    colorselect.set_current_color(gtk.gdk.Color(current_color))
    colorselect.connect("color_changed", lambda widget: set_led_color(__to_hex(colorselect.get_current_color()), False))
    if dialog.run() != gtk.RESPONSE_OK:
        set_led_color(current_color, False)
        logger.warn('No color selected.')
    else:
        set_led_color(__to_hex(colorselect.get_current_color()))
    dialog.destroy()


def set_led_color(color, persist=True):
    color = __parseColor(color)
    hex = "#%0.2x%0.2x%0.2x" % color
    device_path = find_device_path()
    # set the color
    __send("0x010x000x040x000x090x000x000x230x2d0xb30x010x000x000x000x000x000x000x000x010x000x000x000x200x%0.2x0x%0.2x0x%0.2x" % color, device_path)
    # probably commit
    __send("0x010x000x010x000x0a0x000x000x230x2d0xb30x01", device_path)
    if persist is True:
        logger.debug("persisting led color as " + hex + " for device " + device_path)
        Config(hex).write()


def __send(report, device_path):
    eval("echo " + report + " | xxd -r -p > " + device_path)


def __parseColor(color):
    try:
        return webcolors.name_to_rgb(color)
    except ValueError:
        if not color.startswith('#'):
            color = "#" + color
        return webcolors.hex_to_rgb(color)


def __to_hex(color):
    return "#%0.2x%0.2x%0.2x" % (color.red / 256, color.green / 256, color.blue / 256)


class Config:

    def __init__(self, color):
        self.color = color

    def write(self):
        config = {
            'color': self.color
        }
        with open(os.path.expanduser("~") + '/' + CONFIG_FILE_NAME, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    @staticmethod
    def read():
        try:
            with open(os.path.expanduser("~") + '/' + CONFIG_FILE_NAME, 'r') as f:
                config = yaml.load(f)
                return Config(config['color'])
        except IOError:
            return Config('#40e0d0')


class PrismIndicator:

    def __init__(self):
        self.__isopen = False
        reload()
        indicator = appindicator.Indicator("PrismIndicator", os.path.dirname(os.path.realpath(__file__)) + "/steelseries.png", appindicator.CATEGORY_HARDWARE)
        indicator.set_status(appindicator.STATUS_ACTIVE)
        menu = gtk.Menu()
        color_picker = gtk.MenuItem("Change color")
        color_picker.connect("activate", self.pick_color)
        menu.append(color_picker)
        menu.show_all()
        indicator.set_menu(menu)
        gtk.main()

    def pick_color(self, item):
        if self.__isopen is False:
            self.__isopen = True
            prompt_for_led_color()
            self.__isopen = False
        else:
            logger.warn("color picker dialog is already open ... ignoring")


def main():
    # a simple console logger
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)-7s [%(name)s] %(message)s"))
    logging.getLogger().addHandler(console)
    logging.getLogger().setLevel(logging.DEBUG)
    # command line arguments
    parser = argparse.ArgumentParser(description="A tool to configure the SteelSeries Elite Prism HeadSet")
    parser.add_argument("--set-color", type=str, metavar="COLOR", help="set the color to the given valid css color name or hex string and exit")
    parser.add_argument("--reload", default=None, action='store_true', help="reload settings from the config file and exit")
    parser.add_argument("--as-indicator", default=None, action='store_true', help="start a panel indicator")

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.set_color is not None:
            set_led_color(args.set_color)
        elif args.reload is not None:
            reload()
        elif args.as_indicator is not None:
            PrismIndicator()
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
