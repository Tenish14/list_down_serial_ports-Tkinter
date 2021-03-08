# Imports
import tkinter as tk
import serial
from serial.tools.list_ports import comports

# Define constants used throughout the program
PORT = 'COM6'
BAUD_RATE = 9600
TIMEOUT = 0

# Initialize the serial communication and GUI
Device = serial.Serial(baudrate=BAUD_RATE, timeout=TIMEOUT)
root = tk.Tk()
root.title('Serial Communication')


def initDevice(com=PORT):
    print("Connection to:", com)
    Device.port = com

    try:
        Device.open()
        print("Connection with Device successfully opened")
        return True
    except (FileNotFoundError, OSError):
        print("ERROR: Can't connect to this port!")
        return False


def reading():
    try:
        read = Device.read(3)
        string = read.decode().strip()
        return int(string)
    except:
        return 'N\A'


sel = tk.StringVar()
sel.set('Rescan to see available ports')
sel.trace('w', lambda *args: initDevice(sel.get()))

options = tk.OptionMenu(root, sel, [])


def listPorts():
    ports = [port.device for port in comports()]
    print("Ports found:", ports)
    menu = options['menu']
    menu.delete(0, 'end')
    if len(ports) == 0:
        sel.set('No ports found. rescan again')
    else:
        for port in ports:
            menu.add_command(label=port, command=lambda p=port: sel.set(p))
        sel.set('Choose a port:')


refreshPorts = tk.Button(root, text='Refresh COM ports', command=listPorts)

label = tk.Label(root)

refreshPorts.pack(side='top')
options.pack()
label.pack()

root.config()
root.mainloop()