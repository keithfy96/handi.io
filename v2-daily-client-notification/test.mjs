import axios from "axios";

function createGetReqeuest() {
  const airtableBaseId = "apphm9UXhxUdXQz5K";

  const airtableAccessToken =
    "patnEBZvua4RxDWnE.7e4eceea5759d978b80dbb1e9bb8d346039e2ece60b1560f02145ec727f07bcc";

  const airtableRequestHeader = {
    Authorization: `Bearer ${airtableAccessToken}`,
  };

  const options = {
    headers: airtableRequestHeader,
  };

  const airtableRequestUrl = `https://api.airtable.com/v0/${airtableBaseId}`;

  // query string obtained from airtable API encoder
  const queryString = `OR(%0A++++AND(%0A++++++DATETIME_DIFF(%7B1st+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B1st+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%2C%0A++++AND(%0A++++++DATETIME_DIFF(%7B2nd+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B2nd+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%2C%0A++++AND(%0A++++++DATETIME_DIFF(%7B3rd+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B3rd+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%2C%0A++++AND(%0A++++++DATETIME_DIFF(%7B4th+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B4th+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%0A++)`;
  const fullUrl = `${airtableRequestUrl}/Services?filterByFormula=${queryString}`;
  return { fullUrl, options };
}

async function getAirtableData() {
  const response = await axios.get(fullUrl, options);
  const data = response.data;
  console.log(data);
  return data;
}

const { fullUrl, options } = createGetReqeuest();
const data = getAirtableData();
