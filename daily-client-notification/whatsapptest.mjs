// const axios = require("axios");
import axios from "axios";

const notifications = [
  {
    id: "rec2hb8PHtHU1VF18",
    name: "Keith-test-1",
    phoneNumber: "6590057735",
    serviceName: "Floor Servicing",
    jobDate: "November 28, 2023",
    jobTime: "10:30 AM",
  },
  {
    id: "recNH5PLE748JW9X2",
    name: "keith-test-2",
    phoneNumber: "6590057735",
    serviceName: "Cleaning",
    jobDate: "November 28, 2023",
    jobTime: "10:19 AM",
  },
];

const headers = {
  "Content-Type": "application/json",
};

notifications.forEach((notification) => {
  const { clientName, serviceName, phoneNumber, jobDate, jobTime } =
    notification;
  const params = {
    channel: "whatsappcloudapi",
    from: "6587872399",
    to: phoneNumber,
    messageType: "template",
    extendedMessage: {
      WhatsappCloudApiTemplateMessageObject: {
        templateName: "reminder_appointment_2",
        language: "en_GB",
        components: [
          {
            type: "body",
            parameters: [
              { type: "text", text: clientName },
              { type: "text", text: serviceName },
              { type: "text", text: jobDate },
              { type: "text", text: jobTime },
            ],
          },
        ],
      },
    },
  };
  axios
    .post(
      "https://api.sleekflow.io/API/Message/Send/json?apikey=aHAeCHAnHGL8RXkXqh2f7dJIKJA9GNZKx9bFfllE",
      params,
      {
        headers: headers,
      }
    )
    .then((response) => console.log(response.data))
    .catch((error) => console.error(error));
});

const output = { type: "success", message: "finished!" };
