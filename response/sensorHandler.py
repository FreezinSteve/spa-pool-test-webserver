from response.requestHandler import RequestHandler
from io import StringIO
import random
import os


class SensorHandler(RequestHandler):
    temperature = random.randint(0, 300) / 10

    def __init__(self):
        super().__init__()
        self.contentType = "text/plain"

    def get_data(self, parameters):

        id = None
        day = None
        if "id" in parameters:
            id = parameters["id"][0]
        if "day" in parameters:
            day = parameters["day"][0]
        if id is None:
            self.setStatus(404)
            return False

        try:
            self.setStatus(200)
            if day is None:
                # sensor value only
                SensorHandler.temperature = SensorHandler.temperature + random.randint(-10, 10) / 10
                data = str(round(SensorHandler.temperature, 1))
            else:
                filepath = os.getcwd() + "/data/" + id + "." + day
                if os.path.exists(filepath):
                    f = open(filepath, 'r')
                    data = f.read()
                    f.close()
                else:
                    data = ""

            self.contents = StringIO(data)
            if SensorHandler.temperature < 0:
                SensorHandler.temperature += 10
            return True
        except:
            self.setStatus(404)
            return False
