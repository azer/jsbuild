var %(name)s = (function(globals,undefined){

  var _jsbuild_ = (function(){

    var cache = {},
      excinfo = new Error(),
      workingDir = getDir( excinfo.fileName || excinfo.sourceURL );

    function Module(){
      this.exports = null;
      this.fileName = null;
      this.id = null;
      this.workingDir = null;
      this.wrapper = null;
    };

    Module.prototype.call = function(){
      this.exports = {};
      return this.wrapper.call(this, this.exports, this, partial(require, [ this.workingDir ], null));
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
      return path.replace(/\/?[^\/]+$/,"");
    }

    function getId(path){
      var name = path.match(/\/([\w_-]+)\.js$/);
      name && ( name = name[1] );
      return name;
    };

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
        wd = wd.replace(new RegExp("(\\/\\w+){"+lvl+"}$"),'');
        path = path.replace(new RegExp("(\\.\\.\\/){"+lvl+"}"),'');
      };
       
      return ( wd && wd+'/' || '' )+path;
    };

    function require(workingDir,path){

      !/\.js(\?.*)?$/.test(path) && ( path = path+'.js' );

      var uri = resolvePath(path,workingDir), mod = cache[uri];

      mod.exports==null && mod.call();

      return mod.exports;
    };

    return {
      "Module":Module,
      "cache":cache,
      "defineModule":defineModule,
      "getDir":getDir,
      "getId":getId,
      "partial":partial,
      "resolvePath":resolvePath,
      "require":require,
      "workingDir":workingDir
    };

  })();

  return {
    '_jsbuild_':_jsbuild_,
    'require':_jsbuild_.partial(_jsbuild_.require,[''])
  };

})(this); 

%(content)s
