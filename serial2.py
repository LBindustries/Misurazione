import serial
import db
import datetime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import struct

device = "/dev/serial/by-id/usb-Texas_Instruments_MSP_Tools_Driver_E7B510511E002100-if00"
baud_rate = 9600

serial_port = serial.Serial(device, baud_rate, timeout=None)
if not serial_port.isOpen():
    serial_port.open()

serial_port.flushInput()
serial_port.flushOutput()

scheduler = BackgroundScheduler()
scheduler.start()


def read_temperature():
    serial_port.write(str.encode("getq"))
    return int.from_bytes(serial_port.read(), byteorder="big", signed=False)


def calc_special_avg(l: list):
    f = sorted(l)[5:15]
    return sum(f) / len(f)


def job():
    session = db.Session()
    readings = list()
    for reading in range(0, 20):
        readings.append(read_temperature())
    average = calc_special_avg(readings)
    session.add(db.Registrazione(orario=datetime.datetime.now(), valore=average))


scheduler.add_job(job, CronTrigger(second=0))
