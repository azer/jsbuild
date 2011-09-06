var render = require('./templating').render,
    compose = require('functools').compose,
    combiner = require('combiner');


var middleware = {
  'map':[],
  'filter':[filterFilename],
  'reduce':reduceFilenames
};

function buildPackage(options, callback){
  render({ 'template':'package.js', 'view':options, 'partials':options }, callback);
}

function collectModules(workingDir,callback){
  workingDir[workingDir.length-1] != '/' && ( workingDir = workingDir+'/' );
  workingDir = workingDir.replace(/^\.\//,'');

  var chain = compose.async(combiner.findFiles,
    combiner.includeDirectories,
    combiner.flatten,
    removeWorkingDir(workingDir),
    combiner.filter,
    combiner.map,
    combiner.reduce);

  combiner.middleware = middleware;
  chain([workingDir || './'], callback);
}

function filterFilename(filename,callback){

  var matching;

  while(matching = filename.match(/^node_modules\/[^\/]+\//)){
    filename = filename.replace(matching,'');
  }

  callback((/^lib\//).test(filename) && /\.js$/.test(filename));
}

function reduceFilenames(a,b,callback){
  if(!Array.isArray(a)){
    a = [a];
  }

  a.push(b);

  callback(undefined,a);
}

function removeWorkingDir(wd){
  return function(list,callback){
    callback(undefined,list.map(function(el){
      return el.replace(wd,'');
    }));
  }
}

function wrapModule(options, callback){
  render({ 'template':'module.js', 'view':options }, callback);
}

module.exports = {
  'wrapModule':wrapModule,
  'buildPackage':buildPackage,
  'collectModules':collectModules,
  'filterFilename':filterFilename
}
