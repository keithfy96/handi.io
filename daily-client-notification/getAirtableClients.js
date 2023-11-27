// const { DateTime } = require("luxon");
const http = require("https");
const fs = require("fs");
const path = require("path");
const { request } = require("http");
const { log } = require("console");

// --------------------
// logging
// -------------------

function logToFile(message) {
  const logEntry = `${message}\n`;

  // Get the directory path from the file path
  const directoryPath = path.dirname("./output.log");

  // Ensure the directory exists, create it if not
  if (!fs.existsSync(directoryPath)) {
    fs.mkdirSync(directoryPath, { recursive: true });
  }

  // Use the fs.writeFile function to create or overwrite the file with the new log entry
  fs.writeFile("./output.log", logEntry, (err) => {
    if (err) {
      console.error(`Error writing to file: ${err.message}`);
    } else {
      console.log(`Data has been logged `);
    }
  });
}

function saveJsonToFile(jsonObject) {
  // Convert the JSON object to a string with indentation for better readability
  const jsonString = JSON.stringify(jsonObject, null, 2);

  // Use fs.writeFile to save the JSON string to a file
  fs.writeFile("./output.json", jsonString, (error) => {
    if (error) {
      console.error(`Error saving JSON to file: ${error.message}`);
    } else {
      console.log(`JSON data has been saved`);
    }
  });
}

// -----------------------------
// Airtable Table Helper Functions
// -------------------------

function getData() {
  const url = createUrl();
  console.log(`url = ${url}`);
  const options = createOptions();
  console.log(JSON.stringify(options, null, 2));

  const data = getAirtableData();
  // console.log(data);
}

// data validation
function validateData(data) {
  // check if records in the response
  console.log(data);
  if (!data.records) {
    logToFile("records object not present in data response");
    throw new Error("records object not present in data response");
  }
  // check length if < 1
  if (data.records.length < 1) {
    logToFile("no records present in record object");
    throw new Error("no records present in record object");
  }

  return data;
}

// create the list of clients that will recieve messages
function createClientList({ records }) {
  // empty list
  const airTableClients = [];
  // for record in airtableData
  // python method was to check if "Client", "Client Name (from Client)", "Phone Number (from Client)" in record fields (it a list as a property from the row object)
  // new method using multiple maps
  const filteredRecords = records.filter((record) => {
    const fields = record.fields;
    return (
      fields.Client &&
      fields["Phone Number (from Client)"] &&
      fields["Client Name (from Client)"]
    );
  });

  // check if "Phone Number (from Client)" exists
  // saveJsonToFile(filteredRecords)
  // check appointment date
  // if no valid appointment date, return false
  // checkAppointmentDate();
  // format time
  // formatTimeZone();

  return airTableClients;
}

// ---------------------------
// Helper Functions
// ---------------------------

// Setups up url
function createUrl() {
  const airtableBaseId = "apphm9UXhxUdXQz5K";

  const airtableRequestUrl = `https://api.airtable.com/v0/${airtableBaseId}`;
  const airtableServicesUrl = `${airtableRequestUrl}/Services`;
  const airtableServicesFormula = `OR(%0A++++AND(%0A++++++DATETIME_DIFF(%7B1st+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B1st+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%2C%0A++++AND(%0A++++++DATETIME_DIFF(%7B2nd+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B2nd+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%2C%0A++++AND(%0A++++++DATETIME_DIFF(%7B3rd+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B3rd+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%2C%0A++++AND(%0A++++++DATETIME_DIFF(%7B4th+Appointment%7D%2C+NOW()%2C+'hours')+%3E%3D+41%2C%0A++++++DATETIME_DIFF(%7B4th+Appointment%7D%2C+NOW()%2C+'hours')+%3C+65%0A++++)%0A++)`;

  const fullUrl = `${airtableServicesUrl}?filterByFormula=${airtableServicesFormula}`;

  return fullUrl;
}

function createOptions() {
  const airtableAccessToken =
    "patnEBZvua4RxDWnE.7e4eceea5759d978b80dbb1e9bb8d346039e2ece60b1560f02145ec727f07bcc";

  const airtableRequestHeader = {
    Authorization: `Bearer ${airtableAccessToken}`,
  };

  const options = {
    headers: airtableRequestHeader,
  };

  return options;
}

async function getAirtableData(fullUrl, options) {
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

// formats phone number
function formatPhoneNumber(phoneNumber) {
  phoneNumber = phoneNumber.replace(/xa0/g, "");
  phoneNumber = phoneNumber.replace(/[^0-9]/g, "");
  return phoneNumber;
}

// formats timezone
function formatTimezone(dateString) {
  // Parse the input string to create a Date object
  const date = new Date(dateString);

  // Specify the target timezone (Asia/Singapore)
  const targetTimezone = "Asia/Singapore";

  // Get the UTC time from the Date object
  const utcTime = date.getTime() + date.getTimezoneOffset() * 60000;

  // Create a new Date object with the UTC time
  const newDate = new Date(utcTime);

  // Format the new Date object to the target timezone
  const formattedDate = newDate.toLocaleString("en-US", {
    timeZone: targetTimezone,
  });

  return formattedDate;
}

// format the service name
function formatServiceName(service) {
  const serviceName = service["Service"].toLowerCase();

  if (serviceName === "ac") {
    return "Aircon Servicing";
  } else if (serviceName === "fl") {
    return "Floor Servicing";
  } else if (serviceName === "hm") {
    return "Handyman";
  } else if (serviceName === "cl") {
    return "Cleaning";
  } else if ("Servicing Type" in service) {
    return service["Servicing Type"];
  }

  return "";
}

// createClientList helper functions
function checkAppointmentDate() {
  // check which appointment date is in the record is the most relevant by checking which appointment is within 2 days of today
  // checkDateRange() for each appointment
  // if true
  // return type (1st 2nd or 3rd) and date
}

function checkDateRange() {
  // parse date and time
  // check if time difference between today and the appointment date is within 2 days of today
}

function formatTimeZone() {}

// data validation

function main() {
  // import airtable
  // importAirtableBase();
  // send airtable get request & parse json response
  const data = getData();
  // console.log(data);
  // check if the data exists
  // const validatedData = validateData(data);
  // create client list
  // createClientList();
  // check if list > 0

  // return output
}

main();
