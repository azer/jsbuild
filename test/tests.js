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

function test_collectDeps(callback){
  var pkg = { 
    'name':'example-project',
    'manifest':{ 
      'dependencies':{ 
        'dependency':'*',
        'sibling':'*'
      } 
    },
    'workingDir':'test/example-project/',
    'packageDict':{}
  };

  jsbuild.collectDeps(pkg, function(error, deps){
    assert.equal(deps.length, 2);
    assert.equal(deps[0].name, 'dependency');
    assert.equal(deps[0].dependencies[0].name, 'subdependency');
    assert.equal(deps[1].name, 'sibling');
    callback();
  });
}

function test_loadPackage(callback){
  jsbuild.loadPackage('test/example-project/', function(error, pkg){
    if(error){
      throw error;
    }
    assert.equal(pkg.name, 'example-project');
    assert.equal(pkg.manifest.name, 'example-project');
    assert.equal(pkg.manifestPath, 'test/example-project/package.json');
    assert.equal(pkg.dependencies.length, 2);

    var pkgDict = Object.keys(pkg.packageDict);
    assert.equal(pkgDict.length, 4);
    assert.equal(pkgDict[0], 'example-project');
    assert.equal(pkgDict[1], 'dependency');
    assert.equal(pkgDict[2], 'subdependency');
    assert.equal(pkgDict[3], 'sibling');

    assert.equal(pkg.modules.length, 2);
    assert.equal(pkg.modules[1].filename, 'lib/a.js');
    assert.equal(pkg.modules[0].filename, 'lib/b.js');
    callback();
  });
}

function test_collectModules(callback){
  jsbuild.collectModules({ 'workingDir':'test/example-project/' }, function(error, modules){
    try {
      assert.equal(modules.length, 2);
      assert.equal(modules[1].filename, 'lib/a.js');
      assert.equal(modules[0].filename, 'lib/b.js');
      callback();
    } catch(exc) {
      callback(exc);
    }
  });
}

function test_filterFilename(callback){

  var legalPaths = ['foo.js','lib/bar/qux.js','lib/qux/quux.js','node_modules/foo/lib/bar.js'],
      illegalPaths = ['lib/foo','lib/qux.j'];

  for(var i = -1, len=legalPaths.length; ++i < len; ){
    assert.ok(jsbuild.filterFilename(legalPaths[i]));
  };

  for(var i = -1, len=illegalPaths.length; ++i < len; ){
    assert.ok(!jsbuild.filterFilename(illegalPaths[i]));
  };

  callback();
}

function test_loadModule(callback){
  jsbuild.loadModule('test/example-project/lib/a.js', function(error, module){
    assert.equal(module.name, 'a');
    assert.equal(module.filename, 'test/example-project/lib/a.js');
    assert.equal(module.content, 'require(\'dependency\');\nconsole.log(\'a.js\');\n');
    callback();
  });
}

function test_moduleName(callback){
  assert.equal(jsbuild.moduleName('foo.js'),'foo');
  assert.equal(jsbuild.moduleName('foo/bar/qux.js'),'qux');
  assert.equal(jsbuild.moduleName('foo'));
  assert.equal(jsbuild.moduleName('foo/bar/qux'));
  assert.equal(jsbuild.moduleName('foo.js/bar.js/qux'));
  assert.equal(jsbuild.moduleName('foo.js/bar.js/qux.js.'));
  assert.equal(jsbuild.moduleName('qux/quux/c-orge.js'),'c-orge');
  callback();
}

function reset(){

}

module.exports = {
  'test_wrapModule':test_wrapModule,
  'test_buildPackage':test_buildPackage,
  'test_collectModules':test_collectModules,
  'test_filterFilename':test_filterFilename,
  'test_loadPackage':test_loadPackage,
  'test_collectDeps':test_collectDeps,
  'test_loadModule':test_loadModule,
  'test_moduleName':test_moduleName,
  'reset':reset
}
