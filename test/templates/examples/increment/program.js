var inc = require('./increment').increment;
var a = 1;

var puts = typeof alert == 'undefined' && require('sys').puts || alert;

puts('A=' + inc(a));
