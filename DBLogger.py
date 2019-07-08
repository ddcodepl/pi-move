import time
import config


class Logger:
    def __init__(self, location):
        self.location = config.device['location']['_id']

    def save_record(self, recordID, details):
        logs = config.db.logs

        data = {
            "location": self.location,
            "action": recordID,
            "time": int(time.time()),
            "details": details,
            "device": config.device_id
        }

        logs.insert_one(data)

        print('Log with action ID: ' + recordID +
              ' in ' + self.location + ' logged!')
