import time
from evdev import UInput, AbsInfo, ecodes as e, InputDevice, categorize, KeyEvent, list_devices
import select

# Tap note key mappings, feel free to change the keys and tap coordinates
tap_keys = {
    e.KEY_Q: (150, 1525),
    e.KEY_W: (220, 1525),
    e.KEY_E: (290, 1525),
    e.KEY_R: (365, 1525),
    e.KEY_T: (435, 1525),
    e.KEY_Y: (510, 1525),
    e.KEY_U: (575, 1525),
    e.KEY_I: (645, 1525),
    e.KEY_O: (720, 1525),
    e.KEY_P: (790, 1525),
    e.KEY_LEFTBRACE: (860, 1525),
    e.KEY_RIGHTBRACE: (930, 1525),
}

# Flick note key mappings
flick_keys = {
    e.KEY_X: (220, 1525),
    e.KEY_C: (365, 1525),
    e.KEY_SPACE: (500, 1525),
    e.KEY_COMMA: (720, 1525),
    e.KEY_DOT: (860, 1525),
}

all_keys = {**tap_keys, **flick_keys}

# Defines the "capabilities" of the virtual touch device
capabilities = {
    e.EV_ABS: [
        (e.ABS_MT_SLOT, AbsInfo(0, 0, 9, 0, 0, 0)),
        (e.ABS_MT_TRACKING_ID, AbsInfo(0, 0, 65535, 0, 0, 0)),
        (e.ABS_MT_POSITION_X, AbsInfo(0, 0, 1080, 0, 0, 0)),
        (e.ABS_MT_POSITION_Y, AbsInfo(0, 0, 1920, 0, 0, 0)),
    ],
    e.EV_KEY: [e.BTN_TOUCH],
}

ui = UInput(events=capabilities, name="Virtual Touchscreen", version=0x3)

# Detect and listen to a keyboard
keyboard = None
for path in list_devices():
    dev = InputDevice(path)
    if "keyboard" in dev.name.lower() or "kbd" in dev.name.lower():
        keyboard = dev
        break

if not keyboard:
    print("No keyboard found. Now, what in tarnation did you execute the command with?")
    print("Perhaps there are permission issues, try adding your user to the 'input' group.")
    exit(1)

print(f"Listening to keyboard: {keyboard.path}")

tracking_id = 1000
pressed_keys = {}
used_slots = set()

def get_next_free_slot():
    for i in range(10):
        if i not in used_slots:
            return i
    return None

# flick script
def perform_flick(slot, x, y):
    global tracking_id

    ui.write(e.EV_ABS, e.ABS_MT_SLOT, slot)
    ui.write(e.EV_ABS, e.ABS_MT_TRACKING_ID, tracking_id)
    ui.write(e.EV_ABS, e.ABS_MT_POSITION_X, x)
    ui.write(e.EV_ABS, e.ABS_MT_POSITION_Y, y)
    ui.write(e.EV_KEY, e.BTN_TOUCH, 1)
    ui.syn()
    time.sleep(0.005)

    steps = 500 # Unoptimized piece of crap code here, but it was the only way for Project SEKAI to accept the virtual swipe as a flick.
    delta_x = 30
    delta_y = 500

    for i in range(1, steps + 1):
        intermediate_x = x + int(delta_x * i / steps)
        intermediate_y = y - int(delta_y * i / steps)
        ui.write(e.EV_ABS, e.ABS_MT_SLOT, slot)
        ui.write(e.EV_ABS, e.ABS_MT_POSITION_X, intermediate_x)
        ui.write(e.EV_ABS, e.ABS_MT_POSITION_Y, intermediate_y)
        ui.syn()

    ui.write(e.EV_ABS, e.ABS_MT_SLOT, slot)
    ui.write(e.EV_ABS, e.ABS_MT_TRACKING_ID, -1)
    ui.write(e.EV_KEY, e.BTN_TOUCH, 0)
    ui.syn()

    used_slots.discard(slot)
    tracking_id += 1
# end of flick script

# regular tap script
while True:
    r, _, _ = select.select([keyboard.fd], [], [], 0.01)
    for fd in r:
        for event in keyboard.read():
            if event.type == e.EV_KEY:
                key_event = categorize(event)
                code = key_event.scancode

                if code in all_keys:
                    x, y = all_keys[code]

                    if key_event.keystate == KeyEvent.key_down:
                        slot = get_next_free_slot()
                        if slot is None:
                            print("No free multitouch slots! prepare to be ghosted, you 13 fingered alien")
                            continue

                        if code in flick_keys:
                            perform_flick(slot, x, y)
                        else:
                            # Tap begin
                            ui.write(e.EV_ABS, e.ABS_MT_SLOT, slot)
                            ui.write(e.EV_ABS, e.ABS_MT_TRACKING_ID, tracking_id)
                            ui.write(e.EV_ABS, e.ABS_MT_POSITION_X, x)
                            ui.write(e.EV_ABS, e.ABS_MT_POSITION_Y, y)
                            ui.write(e.EV_KEY, e.BTN_TOUCH, 1)
                            ui.syn()

                            pressed_keys[code] = (slot, tracking_id)
                            used_slots.add(slot)
                            tracking_id += 1

                    elif key_event.keystate == KeyEvent.key_up and code in pressed_keys:
                        slot_id, _ = pressed_keys[code]

                        # Tap end
                        ui.write(e.EV_ABS, e.ABS_MT_SLOT, slot_id)
                        ui.write(e.EV_ABS, e.ABS_MT_TRACKING_ID, -1)
                        ui.write(e.EV_KEY, e.BTN_TOUCH, 0)
                        ui.syn()

                        del pressed_keys[code]
                        used_slots.discard(slot_id)

    time.sleep(0.001)
#end of tap script
