# sudo pip install evdev
import evdev
import asyncio
import sys
import requests
import json

print("Avoid pressing keys during startup. Wait until OK for all devices.")
print("Pressing keys during startup causes those keys to get locked up until the device is unplugged.")
print("Press [Esc] to exit")

async def print_events(device, config):
    print("OK: ", device.path)
    while True:
        async for event in device.async_read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                keyevt = evdev.events.KeyEvent(event)
                if(keyevt.keycode == "KEY_ESC"):
                    print("Exiting!")
                    ext()
                    sys.exit(0)
                else:
                    if(keyevt.keystate < 2):
                        # print(device.path, keyevt)
                        url = str(config["ip"])
                        print(url)
                        path = "/"
                        
                        params = {
                            "device": device.path,
                            "state": keyevt.keystate,
                            "scancode": format(keyevt.scancode, "x")
                            }
                        # print(params)
                        try:
                            requests.post(url + path, params=params)
                        except:
                            pass

def ext():
    devices = [evdev.InputDevice("/dev/Macros1")]
    for device in devices:
        try:
            print("Ungrabbing Device: ", device)
            device.ungrab()
        except:
            pass

devices = [evdev.InputDevice("/dev/Macros1")]

config = open("config.json")
config_str = config.read()
config_data = json.loads(config_str)

for device in devices:
    # Does device.capabilities[EV_KEY] not contain BTN_MOUSE?
    if 272 not in device.capabilities()[1]:
        try:
            device.grab()
        except:
            pass
        asyncio.ensure_future(print_events(device, config_data))

loop = asyncio.get_event_loop()
loop.run_forever()
