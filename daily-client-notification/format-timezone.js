function formatTimezone(dateString) {
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

// Example usage
const inputDate = "2023-11-28T02:30:00.000Z";
const result = formatTimezone(inputDate);
console.log(result);
console.log(typeof result);
