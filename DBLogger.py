import time
import config


class Logger:
    def __init__(self, location):
        self.location = config.device['location']['_id']

    def save_record(self, recordID, photo):
        logs = config.db.logs

        data = {
            "location_id": self.location,
            "action_id": recordID,
            "time": int(time.time()),
            "has_photo": photo
        }

        logs.insert_one(data)

        print('Log with action ID: ' + recordID +
              ' in ' + self.location + ' logged!')
