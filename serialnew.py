import serial
import db
import datetime
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
    serial_string = ""
    while "\n" not in serial_string:
        byte = serial_port.read(1)
        string = str(byte, encoding="ascii")
        serial_string += string
    serial_strnumb = serial_string.replace("\n", "")
    return int(serial_strnumb)


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
print("Avvio dello scheduler...")
try:
    scheduler.start()
except KeyboardInterrupt:
    print("Chiusura del programma...")

