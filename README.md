
elite-prism-ctl
--------

a simple tool to configure the SteelSeries Elite Prism Headset on Linux

installation
--------

    git clone https://github.com/mimfgg/elite-prism-ctl.git
    cd elite-prism-ctl
    sudo cp xx-elite-prism.rules /etc/udev/rules.d/94-elite-prism.rules
    sudo restart udev

 unplug/replug your prism soundcard if it was already plugged in, then starts with:

    python ./elite-prism-ctl.py --as-indicator

command line usage
--------

    usage: elite-prism-ctl.py [-h] [--set-color COLOR] [--reload] [--as-indicator]

    A tool to configure the SteelSeries Elite Prism Headset.

    optional arguments:
    -h, --help         show the help message and exit
    --set-color COLOR  set the color to the given valid css color name or hex string and exit
    --reload           reload settings from the configuration file and exit
    --as-indicator     start as a panel indicator
