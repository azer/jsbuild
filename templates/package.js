var {{ package }} = (function(globals,undefined){

  var modules = {};

  function module(filename,wrapper){
    if(!wrapper){
      return modules[filename];
    }

    var wd = dir(filename),
        ctx = undefined;
  
    return (modules[filename] = function(){
      if(!ctx){
        ctx = { 'exports':{} };
        wrapper(ctx, ctx.exports, require(wd), globals);
      }

      return ctx;
    });
  };

  function dir(path){
    return path.replace(/\/?[^\/]*$/,"");
  }

  function resolvePath(path,wd){
    if(path.substring(0,1) == '/' || /^\w+\:\/\//.test(path)){ 
      return path;
    }

    /\/$/.test(wd) && ( wd = wd.substring(0,wd.length-1) );
    /^\.\//.test(path) && ( path = path.substring(2,path.length) );

    if(path.substring(0,3)=='../'){
      var lvl = path.match(/^(?:\.\.\/)+/)[0].match(/\//g).length;
      wd = wd.replace(new RegExp("(\\/?\\w+){"+lvl+"}$"),'');
      path = path.replace(new RegExp("(\\.\\.\\/){"+lvl+"}"),'');
    };
     
    return ( wd && wd+'/' || '' )+path;
  };

  function require(wd){
    return function(filename){
      !/\.js(\?.*)?$/.test(filename) && ( filename+='.js' );
      var uri = /^\./.test(path) && resolvePath(path,workingDir) || path,
          mod = module(uri);  

      if(!mod){ 
        throw new Error('Cannot find module "'+path+'". (Working Dir:'+workingDir+', URI:'+uri+' )');
      }

      return mod();
    }
  };

  return {
    "require":,
    "module":module
  };

})(this); 

{{> modules }}
