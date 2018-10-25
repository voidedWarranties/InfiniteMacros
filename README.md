Example udev rule:
/etc/udev/rules.d/10-local.rules
ACTION=="add", ATTRS{phys}=="usb-3f980000.usb-*/input0", SYMLINK+="Macros1"

How to get your ATTRS{phys}:
udevadm info -a -p  $(udevadm info -q path -n DEVICE NODE)
where DEVICE NODE is the node of your keyboard. (ex: /dev/input/event0)

Depends on evdev, Python 3
sudo pip install evdev

Also, replace the "url" (in the test.py) with the ip of your computer.
You can create a simple webserver with AutoHotKey using AHKhttp and AHKsock.
