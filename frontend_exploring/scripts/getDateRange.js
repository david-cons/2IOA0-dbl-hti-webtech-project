const fs = require('fs');

let rawdata = fs.readFileSync('../data.json');
let emails = JSON.parse(rawdata);
emails.sort((a, b) => a.date < b.date ? -1 : 1)

console.log(emails[0].date)
console.log(emails[emails.length -1].date)