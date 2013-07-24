
""" Utilies to abstract the access of the DS18B20 temperature sensors 

This module assumes that all the required kernel modules are installed and
loaded: w1-gpio and w1-therm.  On a raspi, you can simply list these in
/etc/modules and reboot or you can modprobe them as well.

Sensors are specified by hardward address or by index if you defined a list in
you configuration file.  Ex.:

    brewcontrol.tempsensor = 4a8af1c 4a81c56

You will then be able to access the first sensor either with the string
'4a8af1c' or with the integer 1.  
"""

import os
from time import sleep
from pyramid.settings import aslist
from pyramid.paster import get_appsettings
from pyramid.config import aslist
from pyramid.threadlocal import get_current_registry

W1_DIR = "/sys/bus/w1/devices/"
W1_PREFIX = "28-00000"
W1_SUFFIX = "w1_slave"

NB_ATTEMPTS = 5  # reading from the sensor does not always work but we can retry


def read_temp(id):
    path = sensor_path(id)
    for i in range(NB_ATTEMPTS):
        output = open(sensor_path).readlines()
        if 'YES' in output[0]:
            return output[1].split('=')[1]
        else:
            time.sleep(0.1)    


def sensor_path(id):
    """Return the file system path of a temperature sensor given an int id 
       or a serial string."""
    if os.isfile(os.path.join(W1_DIR, id)):
        return os.path.join(W1_DIR, id, W1_SUFFIX)
    elif os.isfile(os.path.join(W1_DIR, W1_PREFIX + id)):
        return os.path.join(W1_DIR, W1_PREFIX + id, W1_SUFFIX)
    elif isinstance(id, int):
        settings = get_current_registry().settings
        sensor = aslist(settings["brewcontrol.tempsensors"])[id]
        return os.path.join(W1_DIR, W1_PREFIX + id, W1_SUFFIX)

def path_to_id(path):
    base = os.path.split(path)[0]
    serial = os.path.split(base)[1].replace(W1_PREFIX, '')

    settings = get_current_registry().settings
    sensors = aslist(settings["brewcontrol.tempsensors"])
    
    if serial in sensors:
        return sensors.index(serial) + 1
    return serial

