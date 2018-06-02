import serial
import db
import datetime
import struct
from apscheduler.schedulers.blocking import BlockingScheduler

device = "/dev/ttyACM1"
baud_rate = 9600

serial_port = serial.Serial(device, baud_rate, timeout=None)
if not serial_port.isOpen():
    serial_port.open()

serial_port.flushInput()
serial_port.flushOutput()

scheduler = BlockingScheduler()


def read_temperature():
    print("Lettura in corso...")
    serial_port.write(b"get\n")
    return int(str(serial_port.read(5).strip(), encoding="utf-8"))


def calc_special_avg(l: list):
    f = sorted(l)[5:15]
    return sum(f) / len(f)


def job():
    print("Job avviato.")
    session = db.Session()
    readings = list()
    for reading in range(0, 20):
        lettura = read_temperature()
        readings.append(lettura)
    print("Calcolo...")
    average = calc_special_avg(readings)
    print("Aggiunta al database...")
    session.add(db.Registrazione(orario=datetime.datetime.now(), valore=average))
    session.commit()
    session.close()


scheduler.add_job(job, 'interval', minutes=1)
scheduler.start()
print("Scheduler avviato.")
try:
    # Bad idea, però non mi attento a toglierlo
    while True:
        pass
except:
    scheduler.stop()
