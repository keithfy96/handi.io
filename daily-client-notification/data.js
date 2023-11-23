const http = require("https");

console.log("script start");
const airtableBaseId = "apphm9UXhxUdXQz5K";
const airtableAccessToken =
  "patnEBZvua4RxDWnE.7e4eceea5759d978b80dbb1e9bb8d346039e2ece60b1560f02145ec727f07bcc";

const airtableRequestHeader = {
  Authorization: `Bearer ${airtableAccessToken}`,
};

const options = {
  headers: airtableRequestHeader,
};

const fullUrl =
  "https://api.airtable.com/v0/apphm9UXhxUdXQz5K/Services?filterByFormula=OR(%0A++++AND(%0A++++++DATETIME_DIFF(%7B1st+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B1st+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%2C%0A++++AND(%0A++++++DATETIME_DIFF(%7B2nd+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B2nd+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%2C%0A++++AND(%0A++++++DATETIME_DIFF(%7B3rd+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B3rd+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%2C%0A++++AND(%0A++++++DATETIME_DIFF(%7B4th+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B4th+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%0A++)";

async function getAirtableData() {
  const body = await new Promise((resolve, reject) => {
    const req = http.request(fullUrl, options, (res) => {
      let data = "";

      res.on("data", (chunk) => {
        data += chunk;
      });

      res.on("end", () => {
        const jsonObject = JSON.parse(data);
        resolve(jsonObject);
      });
    });

    req.on("error", (error) => {
      reject(error);
    });

    req.end();
  });
  console.log("http call ran");
  return body;
}

const data = getAirtableData();
data.then((response) => console.log(response));
