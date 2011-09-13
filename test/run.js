var testModule = require('./tests'),
    tests = Object.keys(testModule)
            .filter(function(el){ return el.substring(0,5)=='test_' })
            .map(function(el){ return testModule[el] }),
    puts = require('sys').puts;

var mark = function(){

  var ctr = 0,
      len = tests.length,
      fail = 0;

  return function(test,error){
    ctr++;
    error && fail++;

    process.stdout.write('> '+test.name + ' ('+ctr+'/'+len+' , ' + ( (new Date).getTime() - startTS )/1000+'s) ');
    puts(error ? 'FAIL ('+error.message+', '+error.stack+')' : '  OK');
    testModule.reset();

    if(ctr>=len){
      puts('====');
      puts('Ran '+len+' tests '  + ( fail ? 'with ' + fail + ' fail.' : 'without any error.') );
    }
  }

}();

var test, next, startTS;
(function(i){

  if(i>=tests.length){
    puts('* All tests has been fired.');
    return;
  }

  test = tests[i];
  next = arguments.callee.bind(undefined, i+1);

  puts('Running "'+test.name+'" ...');

  startTS = (new Date).getTime();
  try {
    tests[i](mark.bind(undefined,test));
  } catch(error){
    mark(test,error)
  }

  next();

})(0);
