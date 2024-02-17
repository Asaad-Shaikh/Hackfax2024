//http dependency
const http = require('http');

//code will go asaduuuu\
const serverHandler = (req, res) => {
    // Your handling logic goes here
    //post etc 
};

const server = http.createServer(serverHandler);

server.listen(3000, () => {
    console.log("Server online on port 3000");
    let title = $('div[class = "media-body"] > h3').text();
    console.log(title);
});
