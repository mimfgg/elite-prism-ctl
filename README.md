
elite-prism-ctl
--------

a simple tool to change the color of the SteelSeries Elite Prism HeadSet on Linux


installation
--------

    cp xx-prism.rules /etc/udev/rules.d/94-prism.rules
    sudo restart udev

 unplug/replug your prism soundcard if it was already plugged in, then starts with:

    python ./elite-prism-ctl.py --as-indicator

command line usage
--------

    usage: elite-prism-ctl.py [-h] [--set-color COLOR] [--reload] [--as-indicator]

    A tool to configure the SteelSeries Elite Prism HeadSet.

    optional arguments:
    -h, --help         show the help message and exit
    --set-color COLOR  set the color to the given valid css color name or hex string and exit
    --reload           reload settings from the config file and exit
    --as-indicator     start a panel indicator
