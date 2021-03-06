// Server setup
var express    = require('express');
var app        = express();
var bodyParser = require('body-parser');
var User       = require('./app/models/User')
var session    = require('express-session');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var routes = require('./app/routes/index')

var port = 8080;

app.use('/api', routes);
app.use(session({secret:"hdcbjchssckjskns", resave:false, saveUninitialized:true}));

app.listen(port, "0.0.0.0");
console.log('Server is running on port: ' + port);
