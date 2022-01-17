import requests

# Download all the data from the station and put into the Arduino project data folder so we can re-upload for testing
sensors = ["te","rh","bp","ws","wd","gs","gd"]
url = "http://192.168.1.100/sensor?id={}&day={}"
output_path = "C:/Users/delimas/Documents/Arduino/ESP_Chart_Web_Server/data"
#output_path = "C:/Users/delimas/PycharmProjects/python-webserver-part-2/data"

for day in range(0 ,7):
    for sensor in sensors:
        r = requests.get(url.format(sensor,day))
        with open(output_path +"/" + sensor + "." + str(day), 'w') as f:
            f.write(r.content.decode("utf-8"))
