from dateutil import tz
from datetime import datetime

date = "2023-11-25T02:14:03.000Z"

def formatTimezone(date):
  fromZone = tz.tzutc()
  toZone = tz.gettz('Asia/Singapore')
  date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
  date = date.replace(tzinfo=fromZone)
  date = date.astimezone(toZone)
  return date

print(formatTimezone(date))
print(type(formatTimezone(date)))