var jsbuild = require('../lib/jsbuild'),
    assert = require('assert'),
    fs = require('fs');

function test_wrapModule(callback){
  var module1 = 'package.module(\'./filename\', '
              + 'function(module, exports, require, globals, undefined){'
              + '\n  content'
              + '\n});'

  jsbuild.wrapModule({ 'package':'package', 'filename':'./filename', 'content':'content' },function(error, result){
    assert.equal(result, module1);
    callback(0,1);
  });
}

function test_buildPackage(callback){
  var pkg = fs.readFileSync('templates/package.js').toString().replace('{{ package }}', 'package').replace('{{> modules }}','modules');

  jsbuild.buildPackage({ 'package':'package', 'modules':'\nmodules\n' },function(error, result){
    //assert.equal(result, pkg);
    callback(0,1);
  });
}

function test_collectModules(callback){
  jsbuild.collectModules('./test/example-project',function(error, files){
    var expectedModules = ['lib/a.js',
    'lib/b.js',
    'node_modules/dependency/lib/f.js',
    'node_modules/dependency/lib/g.js',
    'node_modules/dependency/node_modules/subdependency/lib/i.js',
    'node_modules/dependency/node_modules/subdependency/lib/j.js']
    assert.equal(files.length, expectedModules.length);
    for(var i = -1, len=expectedModules.length; ++i < len; ){
      assert.equal(files[i],expectedModules[i]);
    };

    callback();
  });
}

function test_filterFilename(callback){

  var legalPaths = ['lib/foo.js','lib/bar/qux.js','lib/qux/quux.js','node_modules/foo/lib/bar.js'],
      illegalPaths = ['lib/foo','qux.js','lib/qux.j','node_modules/foo/test/qux.js'];

  var testLegals,testIllegals;

  var next;

  (function(i){
    if(i>=legalPaths.length){
      testLegals = true;
      if(testLegals && testIllegals){
        callback();
      }
      return;
    }

    next = arguments.callee.bind(undefined,i+1);

    jsbuild.filterFilename(legalPaths[i],function(result){
      assert.ok(result);
      next();
    });

  })(0);

  (function(i){
    if(i>=illegalPaths.length){
      testIllegals = true;
      if(testLegals && testIllegals){
        callback();
      }
      return;
    }

    next = arguments.callee.bind(undefined,i+1);

    jsbuild.filterFilename(illegalPaths[i],function(result){
      assert.ok(!result);
      next();
    });

  })(0);

}

function reset(){

}

module.exports = {
  'test_wrapModule':test_wrapModule,
  'test_buildPackage':test_buildPackage,
  'test_collectModules':test_collectModules,
  'test_filterFilename':test_filterFilename,
  'reset':reset
}
