var HTTP_PORT = process.env.PORT || 8080;
var path = require("path");
var express = require("express");
var app = express();
app.use(express.static(path.join(__dirname, 'public'))); // to serve static files such as css


// send html files
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "./views/log-in.html"));
});

app.get("/home", (req, res) => {
    res.sendFile(path.join(__dirname, "./views/index.html"));
});
app.get("/capture1", (req, res) => {
    res.sendFile(path.join(__dirname, "./views/capture1.html"));
})

// setup http server to listen on HTTP_PORT
app.listen(HTTP_PORT, function () {
    console.log("Server is running on 8080 port");
});

  // Note: you could also just do app.listen(HTTP_PORT); with no callback function.