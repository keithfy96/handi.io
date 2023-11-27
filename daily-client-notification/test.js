const date = "2023-11-27T02:14:00.000Z";

function checkDateRange(date) {
  const givenDate = new Date(date);
  // Current date
  const currentDate = new Date();
  // Calculate the difference in milliseconds
  const timeDifference = givenDate.getTime() - currentDate.getTime();
  // Calculate the difference in days
  const daysDifference = timeDifference / (1000 * 3600 * 24);
  // Check if the date is within the next 2 days
  if (daysDifference >= 0 && daysDifference <= 2) {
    console.log("The given date is within the next 2 days.");
    return true;
  }
  console.log("The given date is not within the next 2 days.");
  return false;
}

checkDateRange(date);
