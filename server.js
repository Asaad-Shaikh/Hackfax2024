//http dependency
const http = require('http');

//code will go 
const serverHandler = (req, res) => {
    // Your handling logic goes here
    //post etc 
};

const server = http.createServer(serverHandler);

server.listen(3000, () => {
    console.log("Server online on port 3000");
});
