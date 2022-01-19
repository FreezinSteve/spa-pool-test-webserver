import json
import random
import time

from http.server import BaseHTTPRequestHandler
from routes.main import routes
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from response.sensorHandler import SensorHandler
from response.stringHandler import StringResponseHandler
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs

controller_state = "0"
pump_state = "0"
heater_state = "0"
setpoint = "38"


class Server(BaseHTTPRequestHandler):

    def do_HEAD(self):
        return

    def do_POST(self):
        global controller_state
        global pump_state
        global heater_state
        global setpoint
        if self.path == "/update-settings":
            handler = StringResponseHandler()
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            handler.set_response(str(post_body))
            handler.stStatus(200)
            print("update-settings")
        elif self.path == "/reboot":
            handler = StringResponseHandler()
            handler.set_response(str("Module rebooting"))
            handler.setStatus(200)
        elif self.path.startswith("/update?"):
            query = urlparse(self.path).query
            parameters = parse_qs(query)
            if (parameters["param"][0] == "auto"):
                controller_state = parameters["state"][0]
            elif (parameters["param"][0] == "pump"):
                pump_state = parameters["state"][0]
            elif (parameters["param"][0] == "heater"):
                heater_state = parameters["state"][0]
            elif (parameters["param"][0] == "setpoint"):
                setpoint = parameters["value"][0]
            handler = StringResponseHandler()
            handler.set_response(str("OK"))
            handler.setStatus(200)
        else:
            handler = StringResponseHandler()
            handler.set_response("Unknown route")
            handler.setStatus(404)
        self.respond({
            'handler': handler
        })

    def do_GET(self):
        global controller_state
        global pump_state
        global heater_state
        global setpoint

        if self.path == "/":
            handler = StaticHandler()
            handler.find("/index.html")
        elif self.path == "/heapfree":
            handler = StringResponseHandler()
            handler.set_response(str(random.randint(20000, 40000)))
        elif self.path == "/time":
            handler = StringResponseHandler()
            handler.set_response(
                datetime.now().replace(microsecond=0).isoformat())
        elif self.path == "/status":
            handler = StringResponseHandler()
            status = {}
            status["dt"] = datetime.now().replace(microsecond=0).isoformat()
            status["te"] = str(random.randint(200, 400) / 10)     # temperature
            status["sp"] = setpoint
            status["ts"] = "770"

            # controller state 0=manual 1=auto
            # Pump state (0=off, 1=on)
            # Heater state (0=off, 1=on)
            status["cs"] = controller_state
            status["ps"] = pump_state       
            status["hs"] = heater_state     
            json_msg = json.dumps(status)
            handler.set_response(json_msg)
        elif self.path == "/reboot":
            handler = StringResponseHandler()
            handler.set_response("Module rebooting")
        elif self.path == "/read-settings":
            handler = StringResponseHandler()
            handler.set_response(
                '{"ssid":"Casa de Lima","ipaddr":"192.168.1.101","gatewayaddr":"192.168.1.250","proxyaddr":"192.168.1.130"}')
        else:
            # Static files in public folder
            handler = StaticHandler()
            handler.find(self.path)
        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()
        # time.sleep(0.5)
        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        if isinstance(content, bytes):
            return content
        else:
            return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
