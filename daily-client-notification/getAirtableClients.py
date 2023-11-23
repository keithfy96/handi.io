import requests
import threading
import re
import json
from datetime import datetime
from dateutil.parser import parse
from dateutil import tz
# import time

currentTime = datetime.now()

def formatPhoneNumber(phoneNumber):
  phoneNumber = phoneNumber.replace('xa0', '')
  phoneNumber = re.sub("[^0-9]", "", phoneNumber)
  return phoneNumber

def formatTimezone(date):
  fromZone = tz.tzutc()
  toZone = tz.gettz('Asia/Singapore')
  date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
  date = date.replace(tzinfo=fromZone)
  date = date.astimezone(toZone)
  return date

def formatServiceName(service):
  if (service['Service'].lower() == 'ac'):
    return 'Aircon Servicing'
  elif (service['Service'].lower() == 'fl'):
    return 'Floor Servicing'
  elif (service['Service'].lower() == 'hm'):
    return 'Handyman'
  elif (service['Service'].lower() == 'cl'):
    return 'Cleaning'
  elif ('Servicing Type' in service):
    return service['Servicing Type']
  return ''
  
def checkDateRange(date):
  parsedDate = parse(date)
  parsedTime = parsedDate.strftime('%d-%m-%Y')
  diffInTime = datetime.strptime(parsedTime, '%d-%m-%Y') - datetime.strptime(currentTime.strftime('%d-%m-%Y'), '%d-%m-%Y')
  diffInDays = diffInTime.days
  if (diffInDays >= 0 and diffInDays <= 2):
    return True
  return False

def checkAppointmentDate(service):
  if ('1st Appointment' in service):
    formattedDate = checkDateRange(service['1st Appointment'])
    if (formattedDate != False):
      return {
        'type': '1st Appointment',
        'date': service['1st Appointment']
      }
  if ('2nd Appointment' in service):
    formattedDate = checkDateRange(service['2nd Appointment'])
    if (formattedDate != False):
      return {
        'type': '2nd Appointment',
        'date': service['2nd Appointment']
      }
  if ('3rd Appointment' in service):
    formattedDate = checkDateRange(service['3rd Appointment'])
    if (formattedDate != False):
      return {
        'type': '3rd Appointment',
        'date': service['3rd Appointment']
      }
  if ('4th Appointment' in service):
    formattedDate = checkDateRange(service['4th Appointment'])
    if (formattedDate != False):
      return {
        'type': '4th Appointment',
        'date': service['4th Appointment']
      }
  return False

def sleekflowWhatsappRequest(client):
  params = {
    "channel": "whatsappcloudapi",
    "from": "6587872399",
    "to": client["phoneNumber"],
    "messageType": "template",
    "extendedMessage": {
      "WhatsappCloudApiTemplateMessageObject": {
        "templateName": "reminder_appointment_3",
        "language": "en_GB",
        "components": [
          {
            "type": "body",
            "parameters": [
              {
                "type": "text",
                "text": client["name"]
              },
              {
                "type": "text",
                "text": client["serviceName"]
              },
              {
                "type": "text",
                "text": client["date"]
              },
              {
                "type": "text",
                "text": client["time"]
              }
            ]
          }
        ]
      }
    }
  }

  headers = {
    'Content-Type': 'application/json'
  }

  data = requests.post(
    url = "https://api.sleekflow.io/API/Message/Send/json?apikey=aHAeCHAnHGL8RXkXqh2f7dJIKJA9GNZKx9bFfllE",
    data = json.dumps(params),
    headers = headers
  )

  print(data.json())
  return True

print(f"Ran started at: {currentTime.strftime('%c')}")


# import airtable base
airtableBaseId = "appUptkoscF8nJpRo"
airtableAccessToken = "pathWRxSKfs5lHzOr.dcdf30a731edc4f664ea097ded9247739af3e4c62731265837416f01e99ab312"

airtableRequestUrl = f"https://api.airtable.com/v0/{airtableBaseId}"
airtableRequestHeader = {
  "Authorization": f"Bearer {airtableAccessToken}"
}

airtableServicesUrl = f"{airtableRequestUrl}/Services"
airtableServicesFormula = "OR(\
  AND(\
    DATETIME_DIFF({1st Appointment}, NOW(), 'hours') >= 41,\
    DATETIME_DIFF({1st Appointment}, NOW(), 'hours') < 65\
  ),\
  AND(\
    DATETIME_DIFF({2nd Appointment}, NOW(), 'hours') >= 41,\
    DATETIME_DIFF({2nd Appointment}, NOW(), 'hours') < 65\
  ),\
  AND(\
    DATETIME_DIFF({3rd Appointment}, NOW(), 'hours') >= 41,\
    DATETIME_DIFF({3rd Appointment}, NOW(), 'hours') < 65\
  ),\
  AND(\
    DATETIME_DIFF({4th Appointment}, NOW(), 'hours') >= 41,\
    DATETIME_DIFF({4th Appointment}, NOW(), 'hours') < 65\
  )\
)"

#send airtable get request
servicesRequest = requests.get(
  url = airtableServicesUrl, 
  headers = airtableRequestHeader, 
  params = {
    "filterByFormula": airtableServicesFormula,
    "maxRecords": 100,
  }
)

servicesResponse = servicesRequest.json()

# print("service response:")
# print(servicesResponse)

if ('records' not in servicesResponse):
  print('Services request error')

servicesData = servicesResponse['records']

if (len(servicesData) <= 0):
  print('No services filtered.')

airtableClients = []

for serviceData in servicesData:
  if ('fields' not in serviceData):
    continue

  service = serviceData['fields']
  print(service)

  if (
    'Client' not in service or
    'Client Name (from Client)' not in service or
    'Phone Number (from Client)' not in service
  ):
    continue

  if (service['Phone Number (from Client)'] == ''):
    continue

  dateToUse = checkAppointmentDate(service)
  if (dateToUse == False):
    continue

  formattedDate = formatTimezone(dateToUse['date'])

  airtableClients.append({
    'id': service['Client'][0],
    'name': service['Client Name (from Client)'][0],
    'phoneNumber': formatPhoneNumber(service['Phone Number (from Client)'][0]),
    # 'phoneNumber': '6281289520078',
    'serviceName': formatServiceName(service),
    'date': formattedDate.strftime('%d %B, %Y'),
    'time': formattedDate.strftime('%H:%M %p')
  })

print("Airtable clients: ")
print(airtableClients)

if (len(airtableClients) <= 0):
  print('No clients to be notified.')

# if (len(airtableClients) > 0):
#   for client in airtableClients:
#     sleekflowWhatsappRequest(client)
  # threads = [
  #   threading.Thread(target=sleekflowWhatsappRequest, args=(client,))
  #   for client in airtableClients
  # ]
  # for t in threads:
  #   t.start()

print(f"Ran finished at: {currentTime.strftime('%c')}")

output = {'type': 'success', 'message': 'finished!', 'data': airtableClients, 'count': len(airtableClients)}