var mustache = require('mustache'),
    fs = require('fs'),
    config = require('./config'),
    errors = require('./errors');

function render(options,callback){
  fs.readFile(config.TEMPLATES_DIR+'/'+options.template, function(error, bf){
    var result;
    if(!error){
      result = mustache.to_html(bf.toString(), options.view, options.partials);
    }
    callback(error, result);
  });
}

module.exports = {
  'render':render
}
