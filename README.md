Example udev rule:
/etc/udev/rules.d/10-local.rules
ACTION=="add", KERNELS=="1-1.2:1.0", SYMLINK+="Macros1"

How to get your KERNELS:
udevadm info -a -p  $(udevadm info -q path -n DEVICE NODE)
where DEVICE NODE is the node of your keyboard. (ex: /dev/input/event0)

Note: Now that I figure out that the ATTRS{serial} doesn't mean what I think it means, macro keyboard udev rules are now dependent on what port and hub you plug your keyboard into. For instance, my Pi 2 setup uses the following layout:

1-1.2:1.0 1-1.4:1.0
1-1.3:1.0 1-1.5:1.0

where each KERNELS value represents one port on the onboard usb

Depends on evdev, Python 3
sudo pip install evdev

Also, replace the ip (in config.json) with the ip of your computer.
You can create a simple webserver with AutoHotKey using AHKhttp and AHKsock.
