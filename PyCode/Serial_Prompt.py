import serial
import os
import sys
from interTransfer import getOpenCOMS, select_port, COMtoCOM, bcolors, cd, kill, prinHelp, status, writePin, clear,mkdir,rm,popd,pushd
import signal
import subprocess

helpstr = bcolors.FAIL+"""
[*] Usage: [Command] [options] [args]
[*] Supported commands
[*] select_port    :    select a port to write commands to
[*] list           :    list all open ports
[*] COM2COM        :    read value from a given port and write to another port
[*] status         :    check status of given port
"""+bcolors.RESET


def sighandle():
    response = input(
        bcolors.WARNING+"[*] Are you sure you want to quit Y/N"+bcolors.RESET)
    if(response == "Y" or response == "y"):
        sys.exit()
    return None


def reduceSpace(string=""):
    strlist = string.split(" ")
    count = 0
    for i in range(len(strlist)):
        if(strlist[i-count] == ''):
            strlist.remove(strlist[i-count])
        count += 1

    return ''.join(strlist)


def prompt(PS="Serial"):

    commands = {
        "list_ports": getOpenCOMS,
        "select_port": select_port,
        "COM2COM": COMtoCOM,
        "status": status,
        "cd": cd,
        "ls": os.listdir,
        "pwd": os.getcwd,
        "pid": os.getpid,
        "kill": kill,
        "help": prinHelp,
        "write": writePin,
        "cls": clear,
        "clear": clear,
        "mkdir": mkdir,
        "rm"   : rm,
        "pushd" : pushd,
        "popd"  : popd
    }

    while(True):
           is_set = False
           try:
                try:
                    value = input(
                        bcolors.OK+f"{os.getcwd()} #" + PS + "> "+bcolors.RESET)
                    if(reduceSpace(value) == "exit"):
                        break
                    elif(reduceSpace(value) == "select_port" or reduceSpace(value) == 'port'):
                        if(not is_set):
                            commands['port'] = commands[reduceSpace(value)]()
                            is_set = True
                        elif(is_set):
                            commands['port'] = commands[reduceSpace(value)]
                        print(
                            f"{bcolors.OK}[*] {commands['port']} port selected ...{bcolors.RESET}")
                    else:
                        print(
                            f"{bcolors.OK}[*] {commands[reduceSpace(value)]()}{bcolors.RESET}")
                except(KeyError,TypeError):
                    print(bcolors.FAIL +
                          f"\n[*] {value} is not a valid command"+bcolors.RESET)
                    print(bcolors.OK+helpstr+bcolors.RESET)
                    continue
           except KeyboardInterrupt:
                response = input(
                    f"\n{bcolors.WARNING}[*] Are you sure you want to quit [Y/N]: {bcolors.RESET}")
                if(response == 'Y' or response == 'y'):
                    kill()
                else:
                    print(f"{bcolors.OK}[*] Aborted{bcolors.RESET}")
                continue


if __name__ == "__main__":
    prompt()
