var modules = ['corge.js',
  'foo/foo.js',
  'bar/bar.js',
  'bar/qux/eggs.js',
  'bar/quux/spam.js',
  'bar/quux/ham.js'];

var test_api = function(test){
  assert( example._jsbuild_ );
  assert( example._jsbuild_.Module );
  assert( example._jsbuild_.cache );
  assert( example._jsbuild_.defineModule );
  assert( example._jsbuild_.getDir );
  assert( example._jsbuild_.getId );
  assert( example._jsbuild_.partial );
  assert( example._jsbuild_.resolvePath );
  assert( example._jsbuild_.require );
  assert( example.require );
  test.callback();
}

var test_cache = function(test){
  var cache = example._jsbuild_.cache;
  assert( cache );
  for(var i = -1, len=modules.length; ++i < len; ){
    var filename = modules[i];
    compare( cache[filename].fileName, filename); 
  };
  test.callback();
}

var test_resolvePath = function(test){
  var resolvePath = example._jsbuild_.resolvePath;
  compare( resolvePath( '/foo', '/home/azer/' ) , "/foo" );
  compare( resolvePath( 'http://foobar', '/home/azer/' ) , "http://foobar" );
  compare( resolvePath( 'ftp://foobar', '/home/azer/' ) , "ftp://foobar" );
  compare( resolvePath( 'foo', '/home/azer/' ) , "/home/azer/foo" );
  compare( resolvePath( './foo', '/home/azer/' ) , "/home/azer/foo" );
  compare( resolvePath( './foo', '' ) , "foo" );
  compare( resolvePath( '../foo', '/home/azer/' ) , "/home/foo" );
  compare( resolvePath( '../foo', '/home/azer' ) , "/home/foo" );
  compare( resolvePath( '../../foo', '/home/azer/' ) , "foo" );
  test.callback();
}

var test_getDir = function(test){
  var getDir = example._jsbuild_.getDir;
  compare( getDir('foo/bar/qux'), 'foo/bar' );
  compare( getDir('/foo/bar/qux'), '/foo/bar' );
  compare( getDir('./foo/bar/'), './foo/bar' );
  compare( getDir('http://qux.quux/foo/bar/spam.eggs'), 'http://qux.quux/foo/bar' );
  compare( getDir('foo/bar/qux?quux=%corge%&spam=eggs!?'), 'foo/bar' );
  test.callback();
}

var test_getId = function(test){
  var getId = example._jsbuild_.getId;
  compare( getId('foo.js'), 'foo' );
  compare( getId('foo/bar/qux.js'), 'qux' );
  compare( getId('foo/bar/qux.js'), 'qux' );
  compare( getId('foo/bar/q_u-x.js'), 'q_u-x' );
  compare( getId('foo/bar/qux.js'), 'qux' )
  test.callback();
}

var test_require = function(test){
  compare( example.require('./corge'), example.require('corge') );
  var corge = example.require('corge'),
    foo = corge.foo,
    bar = corge.bar,
    eggs = bar.eggs,
    ham = eggs.ham,
    spam = ham.spam;
  
  compare( spam.foo, foo );
  compare( example.require('./bar/bar'), bar );
  test.callback();
}

var test_moduleDefinition = function(test){
  example._jsbuild_.defineModule('new/module.js',function(exports,module,require){
    assert( exports );
    compare( module.id, 'module');
    compare( module.fileName, 'new/module.js');
    compare( module.workingDir, 'new');
    test.callback();
  });
  example.require('./new/module')
}

var test_contextCache = function(test){
  example._jsbuild_.defineModule('spam/eggs.js',function(exports,module,require){
    exports.foo = {};
  });
  example.require('./spam/eggs').foo.bar = 314;
  compare( example.require('./spam/eggs').foo.bar, 314);
  test.callback();
}
