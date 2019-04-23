import telegram
import subprocess
import RPi.GPIO as GPIO
import time
import pymongo
import datetime

SENSOR_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# DB Config
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["movement_tracker"]

# Telegram Config
telegram = telegram.Bot(token='898359191:AAEclbdwNTQ9EvUXKix75pt1D0M3_mvWQqg')
chat_id = 198659984

# Locations list
# # 1 - Attic
# # 2 - Office
locationID = 1

# Camera attached
# # 0 - No
# # 1 - Yes
cameraMounted = 0

# Actions list
# # 1 - Move detected
# # 2 - Move detected and photo taken


def save_record(location=1, action=1):
    logs = db.logs
    data = {
        "location_id": location,
        "action_id": action,
        "time": int(time.time())
    }
    insert = logs.insert_one(data)
    print('record saved')


def move_cb(channel):
    actionID = 1
    save_record(locationID, actionID)

    telegram.send_message(
        chat_id=chat_id, text="Movement detected in attic")
    print('message sent')


def photo_cb(channel):
    actionID = 2
    # Subprocess to take a photo as can't use OpenCV without the screen
    subprocess.call('./photo.sh', shell=True)

    telegram.send_photo(chat_id=chat_id, photo=open('./snap.jpg', 'rb'))
    print('photo sent')

    telegram.send_message(
        chat_id=chat_id, text="Movement detected in attic")
    print('message sent')
    save_record(locationID, actionID)


try:
    print('Started')
    if cameraMounted == 0:
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=move_cb)
    else:
        GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=photo_cb)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print "Finish..."
GPIO.cleanup()
