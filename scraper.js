const puppeteer = require('puppeteer');
const cheerio = require('cheerio');

const url = 'https://mason360.gmu.edu/events';

(async () => {
  // Launch the headless browser
  const browser = await puppeteer.launch();
  
  // Open a new page
  const page = await browser.newPage();
  
  // Navigate to the URL
  await page.goto(url, { waitUntil: 'networkidle0' }); // wait until network is idle
  
  // Use the page content in cheerio
  const content = await page.content();
  const $ = cheerio.load(content);
  const events = [];

  // Select the elements and get the data
  $('div.media-body > h3').each(function () {
    const title = $(this).text().trim();
    events.push(title);
  });

  // Output the events
  console.log(events);
  
  // Close the browser
  await browser.close();
})();
