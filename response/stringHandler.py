import datetime

from response.requestHandler import RequestHandler
from io import StringIO
import random
from datetime import datetime
from datetime import timedelta


class StringResponseHandler(RequestHandler):

    def __init__(self):
        super().__init__()
        self.contentType = "text/plain"

    def set_response(self, response):
        self.setStatus(200)
        self.contents = StringIO(response)
        return True
