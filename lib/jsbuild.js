var render = require('./templating').render,
    compose = require('functools').compose,
    combiner = require('combiner'),
    readFile = require('fs').readFile;

var middleware = {
  'map':[],
  'filter':[]
};

function buildPackage(options, callback){
  render({ 'template':'package.js', 'view':options, 'partials':options }, callback);
}

function collectDeps(pkg, callback){

  var deps = [],
      declaredDepObj = pkg.manifest.dependencies,
      declaredDepList = declaredDepObj && Object.keys(declaredDepObj),
      next;

  if(!declaredDepList || !declaredDepList.length){
    return callback(undefined, deps);
  }

  (function _(i){
    if(i>=declaredDepList.length){
      return callback(undefined,deps);
    }

    next = _.bind(null, i+1);

    var dp = declaredDepList[i],
        path = pkg.workingDir + 'node_modules/' + dp + '/';

    if(pkg.packageDict[dp]){
      return next();
    }

    loadPackage(pkg, path, function(error, subpkg){
      if(error){
        return;
        return callback(error);
      }

      deps.push(subpkg);
      next();
    });

  })(0);
}

function collectModules(pkg, callback){
  compose.async(combiner.findFiles,
    combiner.includeDirectories,
    combiner.flatten,
    function(filenames,callback){
      callback(undefined,filenames.filter(filterFilename));
    },
    function(filenames, callback){
      var modules = [];

      (function _(i){
        if(i>=filenames.length){
          return callback(undefined, modules);
        }

        var next = _.bind(null, i+1);

        loadModule(filenames[i], function(error, module){
          module.filename = module.filename.replace(pkg.workingDir,'');
          if(!error) modules.push(module); 
          next();
        });

      })(0);
    })([pkg.workingDir + 'lib/'],callback);
}

function filterFilename(filename,callback){
  return /\.js$/.test(filename);
}

var loadModule = (function(){

  var template;

  return function(filename, callback){
    readFile(filename, function(error, bf){
      if(error) return callback(error);

      var content = bf.toString(),
          name = moduleName(filename);

      callback(undefined, {
        'name':name,
        'filename':filename,
        'content':content
      });
    });
  }

})();

function loadPackage(/*parentPackage, wd, callback*/){

  var argsLen = arguments.length,
      parentPackage = argsLen == 3 && arguments[0] || undefined,
      wd = arguments[argsLen-2],
      callback = arguments[argsLen-1];

  wd[wd.length-1] != '/' && ( wd = wd+'/' );
  wd = wd.replace(/^\.\//,'');

  var manifestPath = wd + 'package.json',
      manifestSource = undefined, 
      manifest = undefined, 
      dependencies = undefined,
      modules = undefined,
      pkg = undefined,
      i = undefined;

  readFile(manifestPath, function(error, bf){

    if(!error){
      manifestSource = bf.toString(); 
      try {
        manifest = JSON.parse(manifestSource);
      } catch(exc) {
        error = exc;
      }
    }

    if(error){
      return callback(error);
    }

    pkg = {
      'dependencies':dependencies,
      'manifest':manifest,
      'manifestPath':manifestPath,
      'manifestSource':manifestSource,
      'modules':modules,
      'name':manifest.name,
      'parent':parentPackage,
      'packageDict':parentPackage && parentPackage.packageDict || {},
      'workingDir':wd
    };

    pkg.packageDict[pkg.name] = pkg;

    collectDeps(pkg, function(error, deps){
      if(error){
        return callback(error);
      }

      pkg.dependencies = deps;

      collectModules(pkg, function(error, modules){
        pkg.modules = modules; 
        callback(error, pkg); 
      });
    });

  });

}

function moduleName(filename){
  var m = filename.match(/([^\/\.]+)\.js$/);
  return !m ? undefined : m[1];
}

function wrapModule(options, callback){
  render({ 'template':'module.js', 'view':options }, callback);
}

module.exports = {
  'wrapModule':wrapModule,
  'buildPackage':buildPackage,
  'collectModules':collectModules,
  'filterFilename':filterFilename,
  'loadPackage':loadPackage,
  'collectDeps':collectDeps,
  'moduleName':moduleName,
  'loadModule':loadModule
}
