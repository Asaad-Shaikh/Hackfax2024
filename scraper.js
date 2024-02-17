const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const fs = require('fs'); // Include the file system module

const url = 'https://mason360.gmu.edu/events';

(async () => {
  let browser;
  try {
    // Launch the headless browser and ensure the variable is in the correct scope
    browser = await puppeteer.launch();
  
    // Open a new page
    const page = await browser.newPage();
  
    // Navigate to the URL
    await page.goto(url, { waitUntil: 'networkidle0' });
  
    // Use the page content in cheerio
    const content = await page.content();
    const $ = cheerio.load(content);
    const events = [];

    // Select the elements and get the data
    $('div.media-body > h3.media-heading.header-cg--h4').each(function () {
      const title = $(this).text().trim();
      events.push(title);
    });

    // Save the events to a file
    fs.writeFileSync('events.txt', events.join('\n'));

    console.log('Events have been saved to events.txt');
  } catch (error) {
    console.error('An error occurred:', error);
  } finally {
    // Ensure the browser gets closed even if an error occurs
    if (browser) {
      await browser.close();
    }
  }
})();
