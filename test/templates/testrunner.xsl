<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>Tests of <xsl:value-of select='test/@name' /></title>
        <script type="text/javascript" charset="utf-8"><![CDATA[
          (function(exports){
            
            var trident = /msie|trident/i.test(navigator.userAgent);

            var tests = exports.tests = null;
            var recordCreationCounter = exports.recordCreationCounter = 0;
            var scripts = exports.scripts = [];

            if(trident) var sources = exports.sources = null;
            
            var $ = function(id){ 
              return document.getElementById('testrunner-'+id); 
            };

            var each = function(list,fn){
              for(var i=-1,len=list.length; ++i<len;){
                fn( list[i], i, list );
              }
              return list;
            }

            var index = exports.index = function(list,el){
              if(list.indexOf) return list.indexOf(el);
              for(var i=-1,len=list.length; ++i<len;){
                if( list[i] == el ) return i;
              }
              return -1;
            }

            var remove = exports.remove = function(list,index){
              return list.slice(0,index).concat( list.slice(index+1) );
            }

            var clear = exports.clear = function(){
              status('Clearing UI');
              $('info-case').innerHTML=tests.length;
              $('info-time').innerHTML='0.0';
              $('monitor').innerHTML = '';
              progress(0);
            }

            var fetch = exports.fetch = function(url,callback){
              var req = typeof XMLHttpRequest != 'undefined' && new XMLHttpRequest || (function(){
                try { return new ActiveXObject("Msxml2.XMLHTTP.6.0"); }
                  catch (e) {}
                try { return new ActiveXObject("Msxml2.XMLHTTP.3.0"); }
                  catch (e) {}
                try { return new ActiveXObject("Msxml2.XMLHTTP"); }
                  catch (e) {}
                throw new Error("This browser does not support XMLHttpRequest.");
              })();

              req.open('GET',url+"?"+String(Number(new Date())).substring(5),true);
              req.onreadystatechange = function(){
                req.readyState == 4 && req.status == 200 && callback( req );
              }
              req.send(null);
            }

            var findTests = exports.findTests = function(){
              status('Searching tests in global namespace...');
              tests = [];
              for(var key in window){
                if( /^test_/.test( key ) && typeof window[key] == "function" ){ 
                  var fn = window[key];
                  fn.name = key;
                  fn.fname = key;
                  tests.push( fn );
                }
              }

              if( trident ){
                for(var i=-1,len=scripts.length; ++i<len;){
                  var pattern = /(?:var|function)\s+(test_[\w$_-]+)/g;
                  while( match = pattern.exec(sources[i]) ){
                    var name = match[1], value=window[name], ind = index(tests,value);
                    if( name in window && typeof value=="function" && ind==-1 ){
                      value.name = name;
                      tests.push(window[name]);
                    }
                  }
                }
              }

              return tests;
            }

            var init = exports.init = function(){
              status('Initializing...');

              scripts.splice(0);
              scripts.push( $('info-file').getAttribute('data-path') );

              each( $('info-file').getAttribute('data-dependencies').split('|'), function(el){
                /[^\s]+/.test(el) && scripts.push(el);
              });

              load(scripts,set);
            }

            var load = exports.load = function(scripts,callback){
              status('Loading...');
              var tasks = 0;
              var unloaded = scripts.slice(0);
              
              if(trident){
                sources = [];
                var unloadedSources = scripts.slice(0);
                unloadedSources.length && tasks++;
                for(var i=-1,len=scripts.length; ++i<len;){
                  var path = scripts[i];
                  fetch(path,(function(path){
                    return function(req){
                      var ind = index( unloadedSources, path );
                      sources[ index(scripts,path) ] = req.responseText;
                      if(ind>-1){
                        unloadedSources = remove( unloadedSources, ind );
                      }
                      unloadedSources.length == 0 && tasks--;
                      tasks == 0 && callback();
                    }
                  })(path));
                }

              }
              
              unloaded.length && tasks++;
              for(var i=-1,len=scripts.length; ++i<len;){
                var url = scripts[i]+"?"+String(Number(new Date())).substring(5);
                var script = document.createElement('script');
                script.type = 'text/javascript';
                script.async = "true";
                script.src = url;
                script.onload = script.onreadystatechange = function(){
                  var path = this.getAttribute('src').replace(/\?\d{8}$/,""), readystate = this.readyState;
                  if( readystate && readystate!='complete' && readystate!='loaded') return;
                  var ind = index( unloaded, path );
                  if(ind>-1){
                    unloaded = remove(unloaded, ind);
                  }

                  unloaded.length == 0 && tasks--;
                  tasks == 0 && callback();
                }
                document.documentElement.firstChild.appendChild( script );
              }

              tasks == 0 && callback();
            }

            var log = exports.log = function(){
              var d = new Date();
              var args = Array.prototype.splice.call(arguments,0,0, '<label class="testrunner-monitor-date">'+[d.getFullYear(),(d.getMonth()+1),d.getDate()].join("-")+" "+[d.getHours(),d.getMinutes(),d.getSeconds()].join(":")+"."+d.getMilliseconds()+"</label>" );
              return put( Array.prototype.join.call( arguments, ', ' ), 'Log' );
            };

            var progress = exports.progress = function(percent){
              percent = Math.floor(percent);
              $('progressbar-fill').innerHTML = '&nbsp;'+percent+'%&nbsp;';
              $('progressbar-fill').style.width = percent>5 && percent+'%' || '30px';
            }
          
            var put = exports.put = function(str,cls){
              var rec = document.createElement('div');
              rec.innerHTML = str;
              rec.setAttribute('class','testrunner-monitor-rec '+cls);
              rec.setAttribute('id','testrunner-rec-'+( ++recordCreationCounter ));
              $('monitor').appendChild( rec );
              return rec;
            };

            var run = exports.run = function(callback){
              var container = put('<div style="clear:both"></div>','testrunner-result');
              var statusline = container.childNodes[0];
              var time = 0; 
              var uncompleted = tests.slice(0);

              var uncompletedWrapper = document.createElement('div'),
                  completedWrapper = document.createElement('div'),
                  failedWrapper = document.createElement('div');

              uncompletedWrapper.setAttribute(trident&&'className'||'class','testrunner-tests-wrapper');
              completedWrapper.setAttribute(trident&&'className'||'class','testrunner-tests-wrapper');
              failedWrapper.setAttribute(trident&&'className'||'class','testrunner-tests-wrapper');

              uncompletedWrapper.innerHTML = '<div style="clear:both"></div>';
              completedWrapper.innerHTML = '<div style="clear:both"></div>';
              failedWrapper.innerHTML = '<div style="clear:both"></div>';

              container.insertBefore( uncompletedWrapper, container.lastChild );
              container.insertBefore( completedWrapper, container.lastChild );
              container.insertBefore( failedWrapper, container.lastChild );

              progress(0);

              for(var i=-1,len=tests.length; ++i<len;){
                status('Running tests('+(len-uncompleted.length)+','+len+')');

                var el = document.createElement('ul');
                el.setAttribute(trident&&'className'||'class','testrunner-case testrunner-waiting');
                el.innerHTML+='<li class="testrunner-case-header"><label>Case:</label>'+(tests[i].name||tests[i].fname)+'</li>';

                uncompletedWrapper.insertBefore( el, uncompletedWrapper.lastChild );
                
                test(tests[i],(function(el){
                  return function(result){
                    status('Running tests('+(len-uncompleted.length+1)+','+len+')');
                    var ind = index(uncompleted,result.test); 
                    if( ind == -1 ) return;
                    uncompleted = remove(uncompleted,ind);
                    var diff = ((result.timeEnd-result.timeStart)/1000);
                    time+=diff;
                    el.setAttribute(trident&&'className'||'class','testrunner-case'+(result.error&&' testrunner-error'||' testrunner-success'));
                    el.innerHTML+='<li class="testrunner-case-header"><label>Time:</label>'+diff+'sec</li>';
                    if(result.error){
                      for(var name in result.error){
                        el.innerHTML+='<li><label>'+name+':</label>'+result.error[name]+'</li>';
                      }
                    }

                    var wrapper = ( result.error && failedWrapper || completedWrapper );
                    wrapper.insertBefore( el, wrapper.lastChild );

                    progress( (len-uncompleted.length)*100/len );
                    if( uncompleted.length == 0 ){
                      status('Ready');
                      $('info-time').innerHTML=time+'sec';
                      callback && callback();
                    }
                  }
                })(el));

              }

            };

            var test = exports.test = function(testcase,callback){
              var result = { test:testcase, timeStart:0, timeEnd:0, error:null };
              result.callback = function(){
                result.timeEnd = Number( new Date() );
                callback(result);
              };
              setTimeout(function(){
                try {
                  result.timeStart = Number( new Date() );
                  testcase(result);
                } catch(exc){
                  result.error = exc;
                };
                result.error && result.callback();
              },10);
            }

            var set = exports.set = function(){
              status('Setting Tests...');
              findTests();
              clear();
              log( navigator.userAgent );
              status('Ready');
            }

            var status = exports.status = function(str){ 
              $('info-status').innerHTML=str;
            };

            ( window.addEventListener || window.attachEvent )( ( !window.addEventListener && 'on' || '' )+'load', init, false );

          })( window.testrunner = {} );

          function assert(expr,desc){
              if(!expr){
                throw new Error('Assertion Error'+(desc&&': '+desc||expr));
              }
          };

          function compare(){
            if( arguments[0] != arguments[1] ){
              throw new Error('Comparison Error: '+Array.prototype.join.call(arguments,', '));
            }
          };
        ]]></script>
        <style type="text/css" media="screen">
          html, body { width:100%; height:100%; margin:0; padding:0; color:#333; }
          #testrunner-container { height:100%; background:#fff; font:12px Arial,sans-serif; }
          #testrunner-head { background:#ccc; margin-top:0; padding-top:10px; }
          #testrunner-progressbar { margin:0 20px 10px 20px; background:#fff; }
          #testrunner-progressbar-fill { display:block; width:0%; padding:5px 0; background:rgb(100,180,205); color:#fff; text-align:right; font-weight:bold; }

          #testrunner-nav { background:#ddd; padding:10px 20px; }
          #testrunner-nav-buttons { margin:0 auto; }

          #testrunner-info { list-style:none; padding:0 0 10px 0; margin:0; }
          #testrunner-info li { display:inline; padding:0 5px 10px 0; color:#111; }
          #testrunner-info label { color:#666; }

          #testrunner-monitor { padding:10px 20px; font-size:10px; background:#fff; }

          .testrunner-monitor-date { color:#888; }
          .testrunner-button { display:inline; border:1px outset #ccc; padding:2px 5px; background:#f2f2f2; cursor:pointer; margin-right:2px; }
          .testrunner-button:hover { background:rgb(255,255,175); }

          .testrunner-tests-wrapper { display:block; width:100%; }

          .testrunner-result { padding:10px; }
          .testrunner-result-statusline { font-weight:bold;  }
          .testrunner-case { display:block; float:left; padding:5px; margin:2px; background:#eee; list-style:none; }
          .testrunner-case li { white-space:pre; }
          .testrunner-case li label { font-weight:bold; padding-right:2px; color:#888; }
          .testrunner-success { background:#ddffdd; }
          .testrunner-success li label { color:#337733; }
          .testrunner-error .testrunner-case-header { background:#ffdddd;  }
          .testrunner-error { background:#ffcccc; }
          .testrunner-error li label { color:#cc3333; }
        </style>
      </head>
      <body>
        <div id="testrunner-container">
          <div id='testrunner-head'>
            <div id='testrunner-progressbar'>
              <div id='testrunner-progressbar-fill'></div>
            </div>
            <div id='testrunner-nav'>
              <ul id='testrunner-info'>
                <li>
                  Name: <label id='testrunner-info-name'><xsl:value-of select='test/@name' /></label>
                </li>
                <li>
                  Status: <label id='testrunner-info-status'>Uninitialized</label>
                </li>
                <li>
                  Path: 
                  <label id='testrunner-info-file'>
                    <xsl:attribute name='data-path'>
                      <xsl:value-of select='test/@path' />
                    </xsl:attribute>
                    <xsl:attribute name='data-dependencies'>
                      <xsl:for-each select='test/dependency'>
                        <xsl:value-of select='@path' />|
                      </xsl:for-each>
                    </xsl:attribute>
                    <xsl:value-of select='test/@path' />
                  </label>
                </li>
                <li>
                  Tests: <label id='testrunner-info-case'>0</label>
                </li>
                <li>
                  Time: <label id='testrunner-info-time'>0.0</label>
                </li>
              </ul>
              <div id='testrunner-nav-buttons'>
                <div id='testrunner-nav-run' class='testrunner-button' onclick='testrunner.run()'>Run</div> 
                <div id='testrunner-nav-clear' class='testrunner-button' onclick='testrunner.set()'>Reset</div> 
                <div id='testrunner-nav-reload' class='testrunner-button' onclick='testrunner.load(testrunner.scripts,testrunner.set)'>Reload</div> 
              </div>
            </div>
          </div>
          <div id='testrunner-monitor'></div>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
