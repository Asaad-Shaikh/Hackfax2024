const axios = require('axios');
const cheerio = require('cheerio');

const url = 'https://mason360.gmu.edu/events';

axios.get(url)
  .then(response => {
    const html = response.data;
    const $ = cheerio.load(html);
    // const events = [];

    // // Example: Find event titles assuming they are in <h2> tags.
    // // Note: The actual selector will depend on the website's HTML structure.
    // $('<a href="/rsvp?id=2261991" aria-label="Event link. Linkup Live: A Networking Success Event for Graduate and Professional Students. Friday, 16 February 2024 At 5:30 PM, EST (GMT-5). Van Metre Hall Room 125 and 126. Opens the event page.">Linkup Live: A Networking Success Event for Graduate and Professional Students</a>').each(function() {
    //   const title = $(this).text();
    //   events.push(title);
    // });

    console.log(html);
  })
  .catch(console.error);
