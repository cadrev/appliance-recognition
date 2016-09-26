//
// node-static is used to host the html file
//
var http    = require('http');
var Static  = require('node-static');  
var file    = new Static.Server('./public', { cache: 0 }); // insert for no caching,{cache:0}
var PORT    = 8087;

//
// Setup Primus and it's plug-ins
// Primus is a websocket library for realtime 
// connection between the client and the server
//
var Primus  = require('primus');  
var Emitter = require('primus-emitter');


//
// Setup TCP Server
// 
var net = require('net');


var server = http.createServer(function (request, response) {  

  request.addListener('end', function() {
    file.serve(request, response);
  }).resume();

}).listen(PORT);


//
// Start the Primus library
//
var primus = new Primus(server, {transformer: 'sockjs', parser: 'JSON' });
primus.use('emitter', Emitter);

//
// start socket connections
//
primus.on('connection', function userConnect(spark){
  
})

var server = net.createServer();  
server.on('connection', handleConnection);

//
// Start the TCP socket server for receiving the data
// from the Python script
//
server.listen(9000, function() {  
  console.log('server listening to %j', server.address());
});

//
// TCP functions
//
function handleConnection(conn) {  
  var remoteAddress = conn.remoteAddress + ':' + conn.remotePort;
  console.log('new client connection from %s', remoteAddress);

  conn.on('data', onConnData);
  conn.once('close', onConnClose);
  conn.on('error', onConnError);


 
  function onConnData(d) {
   
   //
   // Waits for an incoming data from the Python script
   // Once the data is received, the data is sent to the
   // client using websockets.
   //
   console.log(d.toString())
   primus.send('prediction',d.toString())

  }

  function onConnClose() {
    console.log('connection from %s closed', remoteAddress);
  }

  function onConnError(err) {
    console.log('Connection %s error: %s', remoteAddress, err.message);
  }
}




console.log('Magic happens at port: ' + PORT);
primus.save(__dirname + '/public/primus.js');
