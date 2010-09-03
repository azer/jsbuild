var %(name)s = (function(globals,undefined){

  var _jsbuild_ = (function(){

    function Module(){
      this.exports = null;
      this.fileName = null;
      this.id = null;
      this.workingDir = null;
      this.wrapper = null;
    };

    Module.prototype.call = function(){
      console.log('calling ',this.fileName,this.wrapper);
      this.exports = {};
      return this.wrapper.call(this, this.exports, this, partial(require, [ this.workingDir ], null));
    };

    function defineModule(path,modwrapper){
      var module = new Module();
      module.wrapper = modwrapper;
      module.fileName = resolvePath(path,workingDir);
      module.id = getId( module.fileName );
      module.workingDir = getDir( module.fileName ); 

      cache[module.fileName] = module;

      console.log('define module',module.fileName);

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
      if(path.substring(0,1) == '/' || /^http\:\/\//.test(path)) return path;
      if(path.substring(0,3)=='../'){
        var lvl = path.match(/^(?:\.\.\/)+/)[0].match(/\//g).length;
        wd = wd.replace(new RegExp("(\\/\\w+){"+lvl+"}$"),'');
        path = path.replace(new RegExp("(\\.\\.\\/){"+lvl+"}"),'');
      }
      return wd+'/'+path;
    };

    function require(workingDir,path){
      var uri = resolvePath(path,workingDir), mod = cache[uri];
      console.log('require ',uri,mod.exports);

      mod.exports==null && mod.call();

      return mod.exports;
    };

    var cache = {},
      excinfo = new Error(),
      workingDir = getDir( excinfo.fileName || excinfo.sourceURL );

    return {
      "Module":Module,
      "cache":cache,
      "defineModule":defineModule,
      "getDir":getDir,
      "getId":getId,
      "resolvePath":resolvePath,
      "require":require,
      "workingDir":workingDir
    };

  })();

  return {
    '_jsbuild_':_jsbuild_
  };

})(this); 
