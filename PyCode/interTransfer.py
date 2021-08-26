import serial
import time
import sys
import os
import signal
import subprocess
import winreg

dirs = []

class bcolors:
    OK      =      "\033[92m"   #GREEN
    WARNING =      "\033[93m"   #YELLOW
    FAIL    =      "\033[91m"   #RED
    RESET   =      "\033[0m"    #RESET COLOR

helpstr = bcolors.FAIL+"""
[*] Usage: [Command] [options] [args]
[*] Supported commands
[*] select_port    :    select a port to write commands to
[*] list           :    list all open ports
[*] COM2COM        :    read value from a given port and write to another port
[*] status         :    check status of given port
"""+bcolors.RESET


def getOpenCOMS(numtoCheck=255):
    coms = []
    if(numtoCheck > 255): sys.stderr.write(f"{bcolors.FAIL}[*] There are 256 COM ports from 0-255")
    for i in range(numtoCheck):
        try:
            with serial.Serial(f'COM{i}',baudrate=115200,timeout=1) as ser:
                if ser.isOpen():
                    coms.append(f'COM{i}')
                    ser.close()
                else:
                    continue
        except serial.SerialException:
            continue
    return coms

"""
commands format

command:type:value

setbaud:baudrate //set baud rate to baudrate

write:A:0:30 // means write analog pin 0 the value 30
write:D:0:54// means write digital pin 0 with value 54

read:A:0 //means reading value analog pin 0
read:D:0 //means reading digital value from pin 0

print:text // means write text to screen
println:text // means write text to screen and append a newline

select_port 
select_port // to select a com port

list // will list all available COM ports

status COMNumber // will tell status of a given COM port (Wether writable or readable or both)

"""

def sendall(command):
    coms = getOpenCOMS()
    print(coms)
    for com in coms:
        try:
            with serial.Serial(com,baudrate=115200,timeout=1) as ser:
                ser.write(bytes(command,encoding="utf-8"))
                ser.close()
        except serial.SerialException:
            print(f"[*] {com} port busy")
            continue

def COMtoCOM():
    try:
        sender =   "COM" + input("[*] Enter source port: ")
        reciever = "COM" + input("[*] Enter the destination port: ")
        baudrate = int(input("[*] Enter baudrate: "))
    
        with serial.Serial(sender,baudrate,timeout=1) as ser1:
            with serial.Serial(reciever,baudrate,timeout=1) as ser2:
                if(ser1.readable()):
                    if(ser2.writable()):
                            print(bcolors.OK+f"[*] Reading message from {sender} port to Buffer ..."+bcolors.RESET)
                            time.sleep(0.5)
                            message = ser1.read()
                            print(bcolors.OK+f"[*] Message bytes: {message}"+bcolors.RESET)
                            print(bcolors.OK+f"[*] Writing message from Buffer at {hex(id(message))} to device at {reciever} port ..."+bcolors.RESET)
                            time.sleep(0.5)
                            ser2.write(message)
                            time.sleep(0.5)
                            print(bcolors.OK+"[*] Done ..."+bcolors.RESET)
                            time.sleep(0.5)
                ser2.close()
        ser1.close()

    except(serial.SerialException,ValueError) as err:
        print(f"{bcolors.FAIL}[*] Error: {err.args[0]}{bcolors.RESET}")
        # print(f"{bcolors.FAIL}[*] Input values are required and should be of proper format{bcolors.RESET}")
        #print(bcolors.FAIL+"[*] Error: Sender port is not readable or Reciever port is not writable"+bcolors.RESET)

def select_port():
    port = 0
    try:
        port = int(input(bcolors.OK+f"[*] Enter port number [0-100]: "+bcolors.RESET))
        if(port > 255 or port < 0): 
            print(bcolors.OK+"[*] port number must be between 0 and 255 inclusive"+bcolors.RESET)
            return None
        coms = getOpenCOMS()
        try:
            coms.index(f"COM{port}")
            return f"COM{port}"
        except ValueError:
            print(bcolors.FAIL+f"[*] COM{port} is not opened"+bcolors.RESET)
    except ValueError:
        print(bcolors.FAIL+"[*] Error: Enter a valid port value"+bcolors.RESET)

def status():
    s = {
        "port"      : "COM",
        "readable"  : False,
        "writable"  : False
        }
        
    try:
        port = int(input("[*] Enter port number: "))
        try:
            s["port"] += f"{port}"
            with serial.Serial(f"COM{port}",baudrate=115200,timeout=1) as ser:
                    s["readable"] = ser.readable()
                    s["writable"] = ser.writable()
                    ser.close()
            return s
        except serial.SerialException:
            print(bcolors.FAIL+f"[*] {s}"+bcolors.RESET)
    except ValueError:
            print(bcolors.FAIL+"[*] Inplut format unrecognized"+bcolors.RESET)

def cd():
    try:
        directory = input("[*] Enter path to directory: ")
        os.chdir(directory)
    except(ValueError,OSError):
        print(bcolors.FAIL+"[*] Error "+bcolors.RESET)

def kill():
    print(bcolors.OK+f"[*] Exiting process with pid {os.getpid()} ..."+bcolors.RESET)
    time.sleep(1)
    signal.raise_signal(signal.SIGILL)

def prinHelp():
    return helpstr

def attachInterrupt():
    try:
        port = int(input(f"[*] Enter port number(0-255): "))
        #pintype = input(f"[*] Enter pintype (A/D): ")
        pin = int(input(f"[*] Enter pin to attach interrupt: "))
        with serial.Serial(f"COM{port}",baudrate=115200,timeout=1) as ser:
            while(ser.read() != 'OK'):
                ser.write(f"attachInterrupt:{pin}")
                time.sleep(0.05)
            ser.close()
    except(ValueError,serial.SerialException) as err:
        print(f"{bcolors.FAIL}[*] Error: {err.args}")


def readPin():
    try:
        port = int(input(f"[*] Enter port number(0-255): "))
        pin =  int(input("[*[ Enter pin to write value to: "))
        pintype = input("[*] Enter the pintype (A/D): ")

        with serial.Serial(f"COM{port}",baudrate=115200,timeout=1) as ser:
                ser.write(f"read:{pintype}:{pin}")
                time.sleep(0.05)
                ser.close()
    except(ValueError,serial.SerialException) as err:
        print(f"{bcolors.FAIL}[*] Error: {err.args}{bcolors.RESET}")

def mkdir():
    try:
        dirname = input("[*] Enter name of directory to create: ")
        os.mkdir(dirname)
    except(ValueError,OSError) as err:
        if(len(dirname) == 0):
            print(f"{bcolors.FAIL}[*] ")
        print(err.strerror)
def clear():
    if(os.name == 'nt'):
        os.system('cls')
    elif(os.name == 'posix'):
        os.system('clear')

def pushd():
    try:
        directory = input(f"{bcolors.OK}[*] Enter directory name: {bcolors.RESET}")
        is_dir = os.path.isdir(directory)
        if(not is_dir):
            print(f"{bcolors.FAIL}[*] {directory} is not a directory {bcolors.RESET}")
            return None
        if(os.path.isabs(directory)):
            os.chdir(directory)
            # dirs.append(directory)
        else:
            directory = os.path.abspath(directory)
            os.chdir(directory)
            # dirs.append(directory)
        dirs.append(directory)
    except (OSError,ValueError) as err:
        return f"{bcolors.FAIL}[*] {err.strerror} {bcolors.RESET}"

def rm():
    try:
        path = input(f"{bcolors.OK} [*] Enter the filepath: {bcolors.RESET}")
        is_dir = os.path.isdir(path)
        if(is_dir):
            os.rmdir(path)
        else:
            os.remove(path)
    except(ValueError,OSError) as err:
        return f"{bcolors.FAIL} [*] {err.strerror} {bcolors.RESET}"

def popd():
    try:
        if(len(dirs) == 0): 
            raise IndexError
        newLength = len(dirs)-2
        dirs.pop()
        os.chdir(dirs[newLength])
    except (OSError,IndexError):
        print(f"{bcolors.FAIL} [*] Stack empty {bcolors.RESET}")



def writePin():
    port_is_set = False #checks if ports has been set
    pintype_is_set = False #checks if the pintype has been set
    pin_value_is_set = False #check if pin value is set
    value_to_write_is_set = False
    serial_is_opened = False

    try:
        port = int(input("[*] Enter the input number: "))
        port_is_set = True
        pintype =  input("[*] Enter the pin type [A/D]: ")
        if(pintype == 'A' or pintype == 'D'): pintype_is_set = True
        pin_value = int(input("[*] Enter the pin value: "))
        if(pin_value >= 0): pin_value_is_set = True
        value_to_write = int(input("[*] Enter value to write: "))
        if(pintype == 'A' and (pin_value >= 0 and pin_value <= 255)) : value_to_write_is_set = True
        if(pintype == 'D' and (pin_value >= 0 and pin_value <= 1))   : value_to_write_is_set = True

        with serial.Serial(f"COM{port}",baudrate=115200,timeout=1) as ser:
            serial_is_opened = True
            ser.write(bytes(f"write:{pintype}:{pin_value}:{value_to_write}",encoding="utf-8"))
            ser.close()

    except(ValueError,serial.SerialException):
        if(not port_is_set):
            print(f"{bcolors.FAIL}[*] Port value has to be set{bcolors.RESET}")
            return None
        if(not pintype_is_set):
            print(f"{bcolors.FAIL}[*] PinType must be set{bcolors.RESET}")
            return None
        if(not pin_value_is_set):
            print(f"{bcolors.FAIL}[*] Pintype must be set{bcolors.RESET}")
            return None
        if(not value_to_write_is_set):
            print(f"{bcolors.FAIL}[*] Value to write to pin{bcolors.RESET}")
            return None
        if(not serial_is_opened):
            print(f"{bcolors.FAIL}[*] COM{port} is not opened{bcolors.RESET}")
