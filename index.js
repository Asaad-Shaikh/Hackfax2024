
    // Now you can use the $ to query the document
    let title = $('div.media-body > h3').text();
    console.log(title); // Will log the text content of the first <h3> within a <div> with the class "media-body"
})();
