const http = require("https");

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

function validateData(data) {
  // check if records in the response
  if (!data.records) {
    throw new Error("records object not present in data response");
  }
  // check length if < 1
  if (data.records.length < 1) {
    throw new Error("no records present in record object");
  }
  console.log("data validated");
}

function createClientList({ records }) {
  const airtableClients = [];
  let filteredRecords = records.filter((record) => {
    const fields = record.fields;
    return (
      fields.Client &&
      fields["Phone Number (from Client)"] &&
      fields["Client Name (from Client)"]
    );
  });
  // check if phone number exists
  filteredRecords = filteredRecords.filter((record) => {
    return record.fields["Phone Number (from Client)"] !== "";
  });

  // check appointment date
  for (const record of filteredRecords) {
    const recordData = record.fields;
    // console.log(recordData);
    console.log(`id = ${recordData.recordID}`);
    console.log(`name = ${recordData["Client Name (from Client)"]}`);
    const dateToUse = checkAppointmentDate(recordData);
    if (!dateToUse) {
      console.log("no valid date");
      continue;
    }
    const formattedDateTime = formatTimezone(dateToUse.date);
    airtableClients.push({
      id: recordData.recordID,
      name: recordData["Client Name (from Client)"][0],
      phoneNumber: formatPhoneNumber(
        recordData["Phone Number (from Client)"][0]
      ),
      serviceName: formatServiceName(recordData),
      jobDate: formattedDateTime.formattedDate,
      jobTime: formattedDateTime.formattedTime,
    });
  }
  return airtableClients;
}

// --------------------------------------
// helper functions for createClientList
// -------------------------------------

function checkAppointmentDate(recordData) {
  if ("1st Appointment" in recordData) {
    const formattedDate = checkDateRange(recordData["1st Appointment"]);
    if (formattedDate !== false) {
      return {
        type: "1st Appointment",
        date: recordData["1st Appointment"],
      };
    }
  }
  if ("2nd Appointment" in recordData) {
    const formattedDate = checkDateRange(recordData["2nd Appointment"]);
    if (formattedDate !== false) {
      return {
        type: "2nd Appointment",
        date: recordData["2nd Appointment"],
      };
    }
  }
  if ("3rd Appointment" in recordData) {
    const formattedDate = checkDateRange(recordData["3rd Appointment"]);
    if (formattedDate !== false) {
      return {
        type: "3rd Appointment",
        date: recordData["3rd Appointment"],
      };
    }
  }
  if ("4th Appointment" in recordData) {
    const formattedDate = checkDateRange(recordData["4th Appointment"]);
    if (formattedDate !== false) {
      return {
        type: "4th Appointment",
        date: recordData["4th Appointment"],
      };
    }
  }
  return false;
}

function formatTimezone(dateString) {
  console.log(`datestring `);
  console.log(dateString);
  const originalDate = new Date(dateString);
  console.log(`origin date ${originalDate}`);
  // Format the date
  const dateFormatter = new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  const timeFormatter = new Intl.DateTimeFormat("en-US", {
    hour: "numeric",
    minute: "numeric",
    hour12: true,
  });

  const formattedDate = dateFormatter.format(originalDate);
  const formattedTime = timeFormatter.format(originalDate);

  const formattedDateTime = { formattedDate, formattedTime };
  console.log(formattedDateTime);

  return formattedDateTime;
}

function checkDateRange(date) {
  const givenDate = new Date(date);
  // Current date
  const currentDate = new Date();
  // Calculate the difference in milliseconds
  const timeDifference = givenDate.getTime() - currentDate.getTime();
  // Calculate the difference in days
  const daysDifference = timeDifference / (1000 * 3600 * 24);
  // Check if the date is within the next 2 days
  console.log(givenDate);
  if (daysDifference >= 0 && daysDifference <= 2) {
    console.log("The given date is within the next 2 days.");
    return true;
  }
  console.log("The given date is not within the next 2 days.");
  return false;
}

function formatPhoneNumber(phoneNumber) {
  phoneNumber = phoneNumber.replace(/xa0/g, "");
  phoneNumber = phoneNumber.replace(/[^0-9]/g, "");
  return phoneNumber;
}

function formatServiceName(recordData) {
  const serviceName = recordData["Service"].toLowerCase();

  if (serviceName === "ac") {
    return "Aircon Servicing";
  } else if (serviceName === "fl") {
    return "Floor Servicing";
  } else if (serviceName === "hm") {
    return "Handyman";
  } else if (serviceName === "cl") {
    return "Cleaning";
  } else if ("Servicing Type" in recordData) {
    return recordData["Servicing Type"];
  }

  return "";
}

// -----------------------------------
// main
// -----------------------------------

const { fullUrl, options } = createGetReqeuest();
const response = getAirtableData();
response.then((responseData) => {
  const data = responseData;
  validateData(data);
  const filteredRecords = createClientList(data);
  console.log(filteredRecords);
});

// keith-test-1 rec2hb8PHtHU1VF18
// keith-test-2 recNH5PLE748JW9X2
// keith-test-3 recs5ZHsDnPmue7AA
// keith-test-4 recevvZl0ItOm3tz6
