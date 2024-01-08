import requests
import json

# phoneNumber = input.get('Phone Number')
jobDate = input.get('Job Date')
jobTime = input.get('Job Time')
serviceName = input.get('Service Name')
serviceUnit = input.get('Service Unit')
serviceNotes = input.get('Service Notes')
clientName = input.get('Client Name')
clientAddress = input.get('Client Address')
clientPhoneNumber = input.get('Client Phone Number')
orderType = input.get('Order Type')
appointmentHistory = input.get('Appointment History')
lastAppointmentDate = input.get('Last Appointment Date')

phoneNumber = '90057735'
# jobDate = '12 may 2023'
# jobTime = '1:00 am'
# serviceName = 'test'
# serviceUnit = 'test2'
# serviceNotes = 'N/A'
# clientName = 'a'
# clientAddress = 'b'
# clientPhoneNumber = 'c'
# orderType = 'test'
# appointmentHistory = 'test appointment history'
# lastAppointmentDate = 'last appointment date'

params = {
  "channel": "whatsappcloudapi",
  "messageType": "template",
  "from": "6580436970",
  "to": phoneNumber,
  "extendedMessage": {
    "WhatsappCloudApiTemplateMessageObject": {
      "templateName": "vendor_schedule_1",
      "language": "en",
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": jobDate if jobDate != "" else "no date specified"
            },
            {
              "type": "text",
              "text": jobTime if jobTime != "" else "no time specified"
            },
            {
              "type": "text",
              "text": serviceName if serviceName != "" else "no service name"
            },
            {
              "type": "text",
              "text": appointmentHistory if appointmentHistory != "" else "N/A"
            },
            {
              "type": "text",
              "text": serviceUnit if serviceUnit != "" else "0"
            },
            {
              "type": "text",
              "text": serviceNotes.replace("\n", "") if serviceNotes != "" else "N/A"
            },
            {
              "type": "text",
              "text": clientName if clientName != "" else "no client name specified"
            },
            {
              "type": "text",
              "text": clientAddress.replace("\n", "")
            },
            {
              "type": "text",
              "text": clientPhoneNumber if clientPhoneNumber != "" else "no client phone specified"
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

print("about to send request")

requestVendor = requests.post(
  url = "https://api.sleekflow.io/API/Message/Send/json?apikey=aHAeCHAnHGL8RXkXqh2f7dJIKJA9GNZKx9bFfllE",
  data = json.dumps(params),
  headers = headers
)

print('\n First message Response')
print(requestVendor.json())

params = {
  "channel": "whatsappcloudapi",
  "from": "6580436970",
  "to": "6587509712",
  "messageType": "template",
  "extendedMessage": {
    "WhatsappCloudApiTemplateMessageObject": {
      "templateName": "vendor_schedule_1",
      "language": "en",
      "components": [
        {
          "type": "body",
          "parameters": [
                        {
              "type": "text",
              "text": jobDate if jobDate != "" else "no date specified"
            },
            {
              "type": "text",
              "text": jobTime if jobTime != "" else "no time specified"
            },
            {
              "type": "text",
              "text": serviceName if serviceName != "" else "no service name"
            },
            {
              "type": "text",
              "text": appointmentHistory if appointmentHistory != "" else "N/A"
            },
            {
              "type": "text",
              "text": serviceUnit if serviceUnit != "" else "0"
            },
            {
              "type": "text",
              "text": serviceNotes.replace("\n", "") if serviceNotes != "" else "N/A"
            },
            {
              "type": "text",
              "text": clientName if clientName != "" else "no client name specified"
            },
            {
              "type": "text",
              "text": clientAddress.replace("\n", "")
            },
            {
              "type": "text",
              "text": clientPhoneNumber if clientPhoneNumber != "" else "no client phone specified"
            },
          ]
        }
      ]
    }
  }
}

print('\n\n')
print('about to send message to operations')
print('\n')

requestCustom = requests.post(
  url = "https://api.sleekflow.io/API/Message/Send/json?apikey=aHAeCHAnHGL8RXkXqh2f7dJIKJA9GNZKx9bFfllE",
  data = json.dumps(params),
  headers = headers
)

print(requestCustom.json())

output = {'type': 'success', 'message': 'finished!'}