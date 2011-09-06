var testModule = require('./tests'),
    tests = Object.keys(testModule)
            .filter(function(el){ return el.substring(0,5)=='test_' })
            .map(function(el){ return testModule[el] }),
    puts = require('sys').puts;

var test, next, startTS;
(function(i){

  if(i>=tests.length){
    puts('====');
    puts('Ran '+tests.length+' tests without any error.');
    return;
  }

  test = tests[i];
  next = arguments.callee.bind(undefined, i+1);

  process.stdout.write('Running "'+test.name+'" ...');

  startTS = (new Date).getTime();
  tests[i](function(error){
    if(error) throw error;
    puts('  OK ('+( (new Date).getTime() - startTS )/1000+'s) ');
    testModule.reset();
    next();
  });

})(0);
