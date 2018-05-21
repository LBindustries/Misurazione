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
    print("Reading temperatures...")
    serial_port.write(str.encode("getq"))
    return serial_port.read()


def calc_special_avg(l: list):
    f = sorted(l)[5:15]
    fagiano = []
    for tumore in f:
        tumore = int.from_bytes(tumore, byteorder='big', signed=False)
        fagiano.append(tumore)
    print(fagiano)
    return sum(fagiano) / len(f)


def job():
    session = db.Session()
    readings = list()
    for reading in range(0, 20):
        readings.append(read_temperature())
        print(readings)
    average = calc_special_avg(readings)
    print(average)
    session.add(db.Registrazione(orario=datetime.datetime.now(), valore=average))
    print("Misurazione riuscita. In attesa...")


scheduler.add_job(job, CronTrigger(second=0))
input("Waiting...")

