import requests
import threading
import re
import json
from datetime import datetime
from dateutil.parser import parse
from dateutil import tz
from operator import itemgetter
# from sys import exit
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

def formatAppointmentHistory (service):
  date = ''
  latestDate = 'N/A'
  now = datetime.now()

  if '1st Appointment' in service:
    formattedDate = formatTimezone(service['1st Appointment']).strftime('%d %B  %Y')
    checkDate = datetime.strptime(service['1st Appointment'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if checkDate < now:
      latestDate = formattedDate
    date += formattedDate + ', '
  if '2nd Appointment' in service:
    formattedDate = formatTimezone(service['2nd Appointment']).strftime('%d %B  %Y')
    checkDate = datetime.strptime(service['2nd Appointment'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if checkDate < now:
      latestDate = formattedDate
    date += formattedDate + ', '
  if '3rd Appointment' in service:
    formattedDate = formatTimezone(service['3rd Appointment']).strftime('%d %B  %Y')
    checkDate = datetime.strptime(service['3rd Appointment'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if checkDate < now:
      latestDate = formattedDate
    date += formattedDate + ', '
  if '4th Appointment' in service:
    formattedDate = formatTimezone(service['4th Appointment']).strftime('%d %B  %Y')
    checkDate = datetime.strptime(service['4th Appointment'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if checkDate < now:
      latestDate = formattedDate
    date += formattedDate + ', '

  return {
    'date': date.rstrip(', '),
    'latestDate': latestDate
  }

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

def sleekflowWhatsappRequest(vendor):
  params = {
    "channel": "whatsappcloudapi",
    "from": "6587872399",
    "to": vendor["phoneNumber"],
    "messageType": "template",
    "extendedMessage": {
      "WhatsappCloudApiTemplateMessageObject": {
        "templateName": "vendor_schedule_v5",
        "language": "en",
        "components": [
          {
            "type": "body",
            "parameters": [
              {
                "type": "text",
                "text": vendor["date"] if vendor["date"] != "" else "no date specified"
              },
              {
                "type": "text",
                "text": vendor["time"] if vendor["time"] != "" else "no time specified"
              },
              {
                "type": "text",
                "text": vendor["serviceName"] if vendor["serviceName"] != "" else "no service name"
              },
              {
                "type": "text",
                "text": vendor["serviceUnit"] if vendor["serviceUnit"] != "" else "0"
              },
              {
                "type": "text",
                "text": vendor["serviceNotes"].replace("\n", "") if vendor["serviceNotes"] != "" else "N/A"
              },
              {
                "type": "text",
                "text": vendor["clientName"] if vendor["clientName"] != "" else "no client name specified"
              },
              {
                "type": "text",
                "text": vendor["clientAddress"].replace("\n", "")
              },
              {
                "type": "text",
                "text": vendor["clientPhoneNumber"] if vendor["clientPhoneNumber"] != "" else "no client phone specified"
              },
              {
                "type": "text",
                "text": vendor["appointmentHistory"] if vendor["appointmentHistory"] != "" else 'N/A'
              },
              {
                "type": "text",
                "text": vendor["lastAppointmentDate"] if vendor["lastAppointmentDate"] != "" else 'N/A'
              },
            ]
          }
        ]
      }
    }
  }

  headers = {
    'Content-Type': 'application/json'
  }

  requestVendor = requests.post(
    url = "https://api.sleekflow.io/API/Message/Send/json?apikey=aHAeCHAnHGL8RXkXqh2f7dJIKJA9GNZKx9bFfllE",
    data = json.dumps(params),
    headers = headers
  )

  print(requestVendor.json())
  print('thread finished!')
  return True

def populateClients(clientIds):
  data = {}
  airtableUsersFormulaFilter = ""

  for client in clientIds:
    airtableUsersFormulaFilter += f"RECORD_ID() = '{client}',"

  airtableUsersUrl = f"{airtableRequestUrl}/Users"
  airtableUsersFormula = f"OR({airtableUsersFormulaFilter.rstrip(',')})"
  usersRequest = requests.get(
    url = airtableUsersUrl, 
    headers = airtableRequestHeader, 
    params = {
      "filterByFormula": airtableUsersFormula,
      "maxRecords": 100,
    }
  )

  usersResponse = usersRequest.json()

  if ('records' not in usersResponse):
    print('User request error')

  usersData = usersResponse['records']

  if (len(usersData) <= 0):
    print('No users filtered.')

  for user in usersData:
    data[user['id']] = user['fields']

  return data

def populateVendors(vendorIds):
  data = {}
  airtableVendorsFormulaFilter = ""

  for vendor in vendorIds:
    airtableVendorsFormulaFilter += f"RECORD_ID() = '{vendor}',"

  airtableVendorsUrl = f"{airtableRequestUrl}/Vendor"
  airtableVendorsFormula = f"OR({airtableVendorsFormulaFilter.rstrip(',')})"
  vendorsRequest = requests.get(
    url = airtableVendorsUrl, 
    headers = airtableRequestHeader, 
    params = {
      "filterByFormula": airtableVendorsFormula,
      "maxRecords": 100,
    }
  )

  vendorsResponse = vendorsRequest.json()

  if ('records' not in vendorsResponse):
    print('Vendor request error')

  vendorsData = vendorsResponse['records']

  if (len(vendorsData) <= 0):
    print('No Vendors filtered.')

  for vendor in vendorsData:
    data[vendor['id']] = vendor['fields']
    
  return data

print(f"Ran started at: {currentTime.strftime('%c')}")

airtableBaseId = "appUptkoscF8nJpRo"
airtableAccessToken = "pathWRxSKfs5lHzOr.dcdf30a731edc4f664ea097ded9247739af3e4c62731265837416f01e99ab312"

airtableRequestUrl = f"https://api.airtable.com/v0/{airtableBaseId}"
airtableRequestHeader = {
  "Authorization": f"Bearer {airtableAccessToken}"
}

airtableServicesUrl = f"{airtableRequestUrl}/Services"
airtableServicesFormula = "OR(\
  AND(\
    DATETIME_DIFF({1st Appointment}, NOW(), 'hours') >= 6,\
    DATETIME_DIFF({1st Appointment}, NOW(), 'hours') < 30\
  ),\
  AND(\
    DATETIME_DIFF({2nd Appointment}, NOW(), 'hours') >= 6,\
    DATETIME_DIFF({2nd Appointment}, NOW(), 'hours') < 30\
  ),\
  AND(\
    DATETIME_DIFF({3rd Appointment}, NOW(), 'hours') >= 6,\
    DATETIME_DIFF({3rd Appointment}, NOW(), 'hours') < 30\
  ),\
  AND(\
    DATETIME_DIFF({4th Appointment}, NOW(), 'hours') >= 6,\
    DATETIME_DIFF({4th Appointment}, NOW(), 'hours') < 30\
  )\
)"
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

vendorIds = []
clientIds = []

for serviceData in servicesData:
  if ('fields' not in serviceData):
    continue

  service = serviceData['fields']

  if (
    'Client' not in service or
    'Vendor' not in service
  ):
    continue

  clientIds.append(service['Client'][0])
  vendorIds.append(service['Vendor'][0])

airtableClients = populateClients(clientIds)
airtableVendors = populateVendors(vendorIds)
# print('airtable clients:')
# print(airtableClients)
# print('airtable vendors:')
# print(airtableVendors)

airtableServices = []

for serviceData in servicesData:
  service = serviceData['fields']

  if (
    'Client' not in service or
    'Vendor' not in service
  ):
    continue

  if (
    service['Vendor'][0] not in airtableVendors or 
    service['Client'][0] not in airtableClients
  ):
    continue

  vendorToUse = airtableVendors[service['Vendor'][0]]
  clientToUse = airtableClients[service['Client'][0]]
  dateToUse = checkAppointmentDate(service)

  if (dateToUse == False):
    continue

  formattedDate = formatTimezone(dateToUse['date'])

  if (
    'Name' not in vendorToUse or
    'Contact Number' not in vendorToUse or 
    'Client Name' not in clientToUse or 
    'Address' not in clientToUse
  ):
    continue

  serviceName = formatServiceName(service)
  if (serviceName == '' or serviceName == None):
    continue

  appointmentHistory = formatAppointmentHistory(service)
  tolog = 'N/A' if 'Units' not in service else service['Units']
  print(f'logged {tolog}')
  airtableServices.append({
    'serviceName': serviceName,
    'serviceUnit': 'N/A' if 'Units' not in service else service['Units'],
    'serviceNotes': 'N/A' if 'Notes' not in service else service['Notes'],
    'vendorName': vendorToUse['Name'],
    'contractSize': f"${0 if 'Contract Size' not in service else service['Contract Size']:,}",
    'phoneNumber': formatPhoneNumber(vendorToUse['Contact Number']),
    # 'phoneNumber': '6281289520078',
    'orderType': 'N/A' if 'Order Type' not in service else service['Order Type'],
    'clientName': clientToUse['Client Name'],
    'clientAddress': clientToUse['Address'],
    'clientPhoneNumber': formatPhoneNumber(clientToUse['Phone Number']) if 'Phone Number' in clientToUse else '',
    'date': formattedDate.strftime('%d %B, %Y'),
    'time': formattedDate.strftime('%H:%M %p'),
    'appointmentHistory': appointmentHistory['date'],
    'lastAppointmentDate': appointmentHistory['latestDate']
  })

airtableServices = sorted(airtableServices, key=itemgetter('time'))
# print(airtableServices)

# threads = [
#   threading.Thread(target=sleekflowWhatsappRequest, args=(vendor,))
#   for vendor in airtableServices
# ]
# for t in threads:
#   t.start()

print(f"Ran finished at: {currentTime.strftime('%c')}")

output = {'type': 'success', 'message': 'finished!', 'data': airtableServices, 'count': len(airtableServices)}