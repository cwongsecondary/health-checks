#!/usr/bin/env python3

import os, shutil, sys, socket, psutil


def check_reboot():
    """Returns True if the computer has a pending reboot"""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
    """Returns True if there isn't enough disk space, False otherwise"""
    du = shutil.disk_usage(disk)

    # Calculate the percentage of free space
    percent_free = 100* du.free / du/total

    # Calculate how many free GB
    gigabytes_free = du.free / 2**30
    if gigabytes_free <  min_gb or percent_free < min_percent:
        return True
    return False


# Wrapper Function, will pass Functions for us
def check_root_full():
    """Returns True if the root partitiion is full, False otherwise"""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)


def check_no_network():
    """Returns True if it fails to resolve Google's URL, False otherwise"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True


def main():
    checks = [
        (check_reboot, "Pending Reboot"),
        (check_root_full,"Root partition full"),
        (check_no_network, "No working Network"),
    ]

    # Show more than 1 message IF more than 1 Check Failed via use of a Boolean Variable
    everything_ok = True

    for check, msg in checks:
        if check():
            print(msg)
            everything_ok=False

    if not everything_ok:
        sys.exit(1)


"""
REPLACED with the Above
    if check_reboot():
        print("Pending Reboot")
        sys.exit(1)
    if check_root_full():
        print("Root partitiion full")
        sys.exit(1)
"""

print("Everything ok")
sys.exit(0)


