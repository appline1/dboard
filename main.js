
var http = require('http'),
 fs = require('fs');
function serveStaticFile(res, path, contentType, responseCode) {
 if(!responseCode) responseCode = 200;
 fs.readFile(__dirname + path, function(err,data) {
 if(err) {
 res.writeHead(500, { 'Content-Type': 'text/plain' });
 res.end('500 - Internal Error');
 } else {
 res.writeHead(responseCode,
 { 'Content-Type': contentType });
 res.end(data);
 }
 });
}
http.createServer(function(req,res){
 // normalize url by removing querystring, optional
 // trailing slash, and making lowercase
 var path = req.url.replace(/\/?(?:\?.*)?$/, '')
 .toLowerCase();
 switch(path) {
 case '':
 serveStaticFile(res, '/public/home.html', 'text/html');
 break;
 case '/about':
 serveStaticFile(res, '/public/about.html', 'text/html');
 break;
 case '/img/logo.jpg':
 serveStaticFile(res, '/public/img/logo.jpg', 'image/jpeg');
 break;
 default:
 serveStaticFile(res, '/public/404.html', 'text/html',
 404);
 break;
 }
}).listen(3000);
console.log('Server started on localhost:3000; press Ctrl-C to terminate....');




// var express = require('express');
// var app = express();
// app.set('port', process.env.PORT || 3000);
// // custom 404 page
// app.use(function(req, res){
//  res.type('text/plain');
//  res.status(404);
//  res.send('404 - Not Found');
// });
// // custom 500 page
// app.use(function(err, req, res, next){
//  console.error(err.stack);
//  res.type('text/plain');
//  res.status(500);
//  res.send('500 - Server Error');
// });
// app.listen(app.get('port'), function(){
//  console.log( 'Express started on http://localhost:' +
//  app.get('port') + '; press Ctrl-C to terminate.' );
// });

// app.get('/', function(req, res){
//  res.type('text/plain');
//  res.send('Meadowlark Travel');
// });
// app.get('/about', function(req, res){
//  res.type('text/plain');
//  res.send('About Meadowlark Travel');
// });
// // custom 404 page
// app.use(function(req, res, next){
//  res.type('text/plain');
//  res.status(404);
//  res.send('404 - Not Found');
// });


