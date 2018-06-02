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


def read_temperature():
    serial_port.write(b"get\n")
    print("In lettura...")
    return int(str(serial_port.read(), encoding="utf8"))


def calc_special_avg(l: list):
    f = sorted(l)[5:15]
    return sum(f) / len(f)


def job():
    session = db.Session()
    print("a")
    readings = list()
    for reading in range(0, 20):
        print("b")
        lettura=read_temperature()
        print(lettura)
        readings.append(lettura)
    average = calc_special_avg(readings)
    print(average)
    session.add(db.Registrazione(orario=datetime.datetime.now(), valore=average))
    session.commit()

scheduler.add_job(job, CronTrigger(second=0))
scheduler.start()
try:
    while True:
        pass
except:
    scheduler.stop()
