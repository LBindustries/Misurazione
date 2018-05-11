import pymysql
import serial
import time
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler

device = "/dev/serial1"
baud_rate = 9600

serial_port = serial.Serial(device, baud_rate, timeout=None)
if not serial_port.isOpen():
    serial_port.open()

serial_port.flushInput()
serial_port.flushOutput()

scheduler = BackgroundScheduler()
scheduler.start()

results = list()


def read_temperature():
    print("Reading temperatures...")
    return serial_port.read()


def calc_special_avg(l: list):
    f = sorted(l)[5:15]
    return sum(f) / len(f)


def job():
    readings = list()
    for reading in range(0, 20):
        readings.append(read_temperature())
    average = calc_special_avg(readings)
    results.append(average)


scheduler.add_job(job, CronTrigger(second=0))
input("Waiting...")
