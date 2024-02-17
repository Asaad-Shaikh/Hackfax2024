const axios = require('axios');
const cheerio = require('cheerio');

const url = 'https://mason360.gmu.edu/events';

axios.get(url)
  .then(response => {
    const html = response.data;
    const $ = cheerio.load(html);
    const events = [];

    // Example: Find event titles assuming they are in <h2> tags.
    // Note: The actual selector will depend on the website's HTML structure.
    $('div[class = "media-body"]>h3').each(function() {
      const title = $(this).text();
      events.push(title);
    });

    console.log(events);
  })
  .catch(console.error);
