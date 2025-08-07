import RPi.GPIO as GPIO
import subprocess
import time
import os

BUTTON_PIN = 26
screen_on = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running command: {cmd}\n{result.stderr.decode()}")
    return result.stdout.decode()

def set_screen(on):
    # requires DISPLAY environment variable
    if on:
        run_cmd('DISPLAY=:0 xset dpms force on')
    else:
        run_cmd('DISPLAY=:0 xset dpms force off')

def set_cpu_governor(mode):
    run_cmd(f'sudo cpufreq-set -g {mode}')

def drop_caches():
    # clear RAM cache
    run_cmd('sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"')

def toggle():
    global screen_on
    if screen_on:
        print("Turning off screen, lowering CPU frequency, clearing RAM cache")
        set_screen(False)
        set_cpu_governor('powersave')
        drop_caches()
    else:
        print("Turning on screen, setting CPU to normal mode")
        set_screen(True)
        set_cpu_governor('ondemand')
    screen_on = not screen_on

def button_callback(channel):
    toggle()

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

print("Ready. Press GPIO26 button to toggle state.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    set_screen(True)
    set_cpu_governor('ondemand')
    print("Program terminated.")

