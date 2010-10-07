var foobar = (function(globals,undefined){

  var jsbuild = (function(){

    var cache = {};

    function Module(){
      this.exports = null;
      this.fileName = null;
      this.id = null;
      this.workingDir = null;
      this.wrapper = null;
    };

    Module.prototype.call = function(){
      this.exports = {};
      return this.wrapper.call(null, this.exports, this, partial(require, [ this.workingDir ], null), globals);
    };

    function defineModule(path,modwrapper){
      var module = new Module();
      module.wrapper = modwrapper;
      module.fileName = path;
      module.id = getId( module.fileName );
      module.workingDir = getDir( module.fileName ); 

      cache[module.fileName] = module;

      return module;
    };

    function getDir(path){
      return path.replace(/\/?[^\/]*$/,"");
    }

    function getId(path){
      var name = path.match(/\/?([\w_-]+)\.js$/);
      name && ( name = name[1] );
      return name;
    };

    function getModuleByFilename(filename){
      return cache[filename];
    }

    function partial(fn,init_args,scope){
      !init_args && ( init_args = [] );
      return function(){
        var args = Array.prototype.slice.call(init_args,0);
        Array.prototype.push.apply(args,arguments);
        return fn.apply(scope,args);
      };
    };

    function resolvePath(path,wd){
      if(path.substring(0,1) == '/' || /^\w+\:\/\//.test(path)) return path;

      /\/$/.test(wd) && ( wd = wd.substring(0,wd.length-1) );
      /^\.\//.test(path) && ( path = path.substring(2,path.length) );

      if(path.substring(0,3)=='../'){
        var lvl = path.match(/^(?:\.\.\/)+/)[0].match(/\//g).length;
        wd = wd.replace(new RegExp("(\\/?\\w+){"+lvl+"}$"),'');
        path = path.replace(new RegExp("(\\.\\.\\/){"+lvl+"}"),'');
      };
       
      return ( wd && wd+'/' || '' )+path;
    };

    function require(workingDir,path){

      !/\.js(\?.*)?$/.test(path) && ( path = path+'.js' );

      var uri = resolvePath(path,workingDir), mod = cache[uri];

      if(!mod) throw new Error('Cannot find module "'+path+'". (Working Dir:'+workingDir+', URI:'+uri+' )')

      mod.exports==null && mod.call();

      return mod.exports;
    };

    return {
      "Module":Module,
      "cache":cache,
      "defineModule":defineModule,
      "getDir":getDir,
      "getId":getId,
      "getModuleByFilename":getModuleByFilename,
      "partial":partial,
      "resolvePath":resolvePath,
      "require":require
    };

  })();

  return {
    '_jsbuild_':jsbuild,
    'require':jsbuild.partial(jsbuild.require,[''])
  };

})(this); 

foobar._jsbuild_.defineModule("math.js",function(exports,module,require,globals,undefined){
 exports.add = function() {
  var sum = 0, i = 0, args = arguments, l = args.length;
  while (i < l) {
    sum += args[i++];
  }   
  return sum;
};  
 
});

foobar._jsbuild_.defineModule("increment.js",function(exports,module,require,globals,undefined){
 var add = require('./math').add;
exports.increment = function(val) {
  return add(val, 1); 
};
 
});

foobar._jsbuild_.defineModule("program.js",function(exports,module,require,globals,undefined){
 var inc = require('./increment').increment;
var a = 1;

var puts = typeof alert == 'undefined' && require('sys').puts || alert;

puts('A=' + inc(a));
 
});


foobar._jsbuild_.getModuleByFilename("program.js").call();
