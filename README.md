# rpi-kiosk-todoist

A minimal Raspberry Pi kiosk setup that runs Todoist in full screen.


### Installation
```
sudo apt install --no-install-recommends xserver-xorg xinit openbox chromium-browser unclutter cpufrequtils
nano ~/.xinitrc
```

In .xinitrc
```
#!/bin/sh
xset +dpms          # Enable DPMS (display power management)
xset s on           # Enable screensaver
xset s 300 300      # Screensaver after 300 seconds (5 min)
unclutter -idle 0 &

python3 "$HOME/rpi-kiosk-todoist/toggle.py" &
openbox &
chromium-browser --kiosk https://todoist.com/app


```

Autostart
```
nano ~/.bashrc

//Add at the end: 
if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
  startx
fi
```

Autologin
```
sudo raspi-config
-> SystemOptions -> Auto Login
```
Then:

sudo reboot


### Power saving button (GPIO26)

```
sudo apt install cpufrequtils
```

the toggle.py script monitors GPIO26 for a button press.

- Turns off the screen 
- Switches CPU to low-power mode 
- Clears RAM cache 

press again to restore normal operation


### Connect Bluetooth Keyboard

```
sudo apt install bluetooth bluez pulseaudio pulseaudio-module-bluetooth

sudo systemctl enable bluetooth
sudo systemctl start bluetooth

bluetoothctl
power on
agent on
default-agent
scan on

//search on the list your keyboard
//for example 
//[NEW] Device AA:BB:CC:DD:EE:FF Bluetooth 5.1 Keyboard

pair AA:BB:CC:DD:EE:FF
connect AA:BB:CC:DD:EE:FF
trust AA:BB:CC:DD:EE:FF

exit

```
