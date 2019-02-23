# sudo pip install evdev
import evdev
import asyncio
import sys
import requests
import json
import time

print("Avoid pressing keys during startup. Wait until OK for all devices.")
print("Pressing keys during startup causes those keys to get locked up until the device is unplugged.")
print("Press [Esc] to exit")

taps = {}

hotstring = ""
hotstring_time = 0

async def print_events(device):
    global taps
    global hotstring
    global hotstring_time
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
                    if(keyevt.keystate == 1):
                        hotstringkey = keyevt.keycode[4:] + "/"
                        hotstring = hotstring + hotstringkey
                        hotstring_time = int(time.time())
                        if(keyevt.scancode in taps):
                            if(taps[keyevt.scancode] != None):
                                taps[keyevt.scancode] = {
                                    "taps": taps[keyevt.scancode]["taps"] + 1,
                                    "time": int(time.time()),
                                    "device": device.path
                                    }
                            else:
                                taps[keyevt.scancode] = {
                                    "taps": 1,
                                    "time": int(time.time()),
                                    "device": device.path
                                    }
                                
                        else:
                            taps[keyevt.scancode] = {
                                "taps": 1,
                                "time": int(time.time()),
                                "device": device.path
                                }
        
                            
                    if(keyevt.keystate < 2):
                        # print(device.path, keyevt)
                        url = str(config_data["ip"])
                        path = "/"

                        tapcount = 1
                        if(keyevt.scancode in taps):
                            if(taps[keyevt.scancode] != None):
                                tapcount = taps[keyevt.scancode]["taps"]
                        params = {
                            "device": device.path,
                            "state": keyevt.keystate,
                            "taps": tapcount,
                            "final": 0,
                            "scancode": format(keyevt.scancode, "x"),
                            "key": keyevt.keycode
                            }
                        # print(params)
                        try:
                            requests.post(url + path, params=params)
                        except:
                            pass

def ext():
    devices = [evdev.InputDevice("/dev/Macros1"), evdev.InputDevice("/dev/Macros2")]
    for device in devices:
        try:
            print("Ungrabbing Device: ", device)
            device.ungrab()
        except:
            pass
    task.cancel()

async def tap_loop():
    global taps
    global hotstring
    global hotstring_time
    while True:
        for key, value in taps.items():
            if(value == None):
                continue
            if(int(time.time()) - taps[key]["time"] >= 1):
                params = {
                    "device": device.path,
                    "state": 3,
                    "taps": taps[key]["taps"],
                    "final": 1,
                    "scancode": format(key, "x")
                    }
                url = str(config_data["ip"])
                path = "/"
                try:
                    requests.post(url + path, params=params)
                except:
                    pass
                taps[key] = None

        if(int(time.time()) - hotstring_time >= 1):
            if(hotstring != "" and hotstring.endswith("ENTER/")):
                params = {
                    "device": device.path,
                    "state": 4,
                    "scancode": "",
                    "hotstring": hotstring
                    }
                url = str(config_data["ip"])
                path = "/"
                try:
                    requests.post(url + path, params=params)
                except:
                    pass
            hotstring = ""
        await asyncio.sleep(1)

devices = [evdev.InputDevice("/dev/Macros1"), evdev.InputDevice("/dev/Macros2")]

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
        asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
task = loop.create_task(tap_loop())
loop.run_forever()
