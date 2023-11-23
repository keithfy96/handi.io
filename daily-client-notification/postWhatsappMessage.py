import requests
import json

phoneNumber = input.get('Phone Number')
jobDate = input.get('Job Date')
jobTime = input.get('Job Time')
serviceName = input.get('Service Name')
clientName = input.get('Client Name')

# phoneNumber = '6281289520078'
# jobDate = '12 may 2023'
# jobTime = '1:00 am'
# serviceName = 'test'
# clientName = 'a'

headers = {
  'Content-Type': 'application/json'
}

params = {
  "channel": "whatsappcloudapi",
  "from": "6587872399",
  "to": phoneNumber,
  "messageType": "template",
  "extendedMessage": {
    "WhatsappCloudApiTemplateMessageObject": {
      "templateName": "reminder_appointment_2",
      "language": "en_GB",
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": clientName
            },
            {
              "type": "text",
              "text": serviceName
            },
            {
              "type": "text",
              "text": jobDate
            },
            {
              "type": "text",
              "text": jobTime
            }
          ]
        }
      ]
    }
  }
}

requestCustom = requests.post(
  url = "https://api.sleekflow.io/API/Message/Send/json?apikey=aHAeCHAnHGL8RXkXqh2f7dJIKJA9GNZKx9bFfllE",
  data = json.dumps(params),
  headers = headers
)

print(requestCustom.json())

output = {'type': 'success', 'message': 'finished!'}