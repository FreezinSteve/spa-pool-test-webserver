import requests
from datetime import datetime
from datetime import timedelta


def get_latest_value(content):
    # Date is '\n' delimited.
    data = content.decode().strip()
    lines = data.split('\n')
    last_line = lines[-1]
    items = last_line.split(',')
    timestamp = datetime.strptime(items[0], '%Y-%m-%dT%H:%M:%S')
    value = float(items[1])
    return (timestamp, value)


def htmlformat_timestamp(timestamp):
    # Date time is in local standard time
    # 2021-10-30T18:20:00
    # Date time needs to be UTC encoded as:
    # YYYY-mm-DD HH:mm:ss, where ':' is encoded as %3A, and the space is encoded as either '+' or %20.
    utc = timestamp - timedelta(minutes=utc_offset)
    html_date = datetime.strftime(utc, '%Y-%m-%d %H:%M:%S')
    html_date = html_date.replace(' ', '%20')
    html_date = html_date.replace(':', '%3A')
    return html_date


def push_to_wow(timestamp, temp, rh, winddir, windspeed, msl):
    # Form the request
    # e.g.
    # http://wow.metoffice.gov.uk/automaticreading?siteid=123456&siteAuthenticationKey=654321&dateutc=2011-02-02+10%3A32%3A55&winddir=230&windspeedmph=12&windgustmph=12&windgustdir=25&humidity=90&dewptf=68.2&tempf=70&rainin=0&dailyrainin=5&baromin=29.1&soiltempf=25&soilmoisture=25&visibility=25&softwaretype=weathersoftware1.0
    url = 'http://wow.metoffice.gov.uk/automaticreading'
    url += '?siteid=' + site_id
    url += '&siteAuthenticationKey=' + site_key
    url += '&dateutc=' + htmlformat_timestamp(timestamp)
    url += '&softwaretype=MyCustomScript1.0'
    url += '&tempf=' + str(round((temp * 1.8) + 32, 2))  # convert from Celsius to Fahrenheit
    url += '&humidity=' + str(rh)
    url += '&winddir=' + str(winddir)
    url += '&windspeedmph=' + str(round(windspeed * 2.237, 1))  # Convert from m/s to mph
    url += '&baromin=' + str(round(msl *  0.02953, 3))     # Convert from hpa to inches Hg
    r = requests.get(url)
    return r.status_code


def main():
    # Get latest temperature
    r = requests.get('http://192.168.1.100/sensor?id=te&day=0')
    time, temp = get_latest_value(r.content)

    r = requests.get('http://192.168.1.100/sensor?id=rh&day=0')
    time, rh = get_latest_value(r.content)

    r = requests.get('http://192.168.1.100/sensor?id=wd&day=0')
    time, winddir = get_latest_value(r.content)

    r = requests.get('http://192.168.1.100/sensor?id=ws&day=0')
    time, windspeed = get_latest_value(r.content)

    r = requests.get('http://192.168.1.100/sensor?id=bp&day=0')
    time, msl = get_latest_value(r.content)

    response = push_to_wow(time, temp, rh, winddir, windspeed, msl)

    print("HTTP Response: " + str(response))


site_id = '235ccda6-9b38-ec11-a3ee-0003ff59b320'
site_key = '19741106'
utc_offset = 720  # minutes
main()
