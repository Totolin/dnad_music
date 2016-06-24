var express = require('express');
var app = express();
var server = require('http').Server(app);

// Make files visible from cwd + other folders
app.use(express.static(__dirname));
//ap#p.use(express.static(__dirname + '/css'));
//app.use(express.static(__dirname + '/images'));
//app.use(express.static(__dirname + '/js'))

server.listen(3000, function(){
    console.log('Listening at port 3000');
});
