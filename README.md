Providing running CommonJS modules on the web without any need of source code modification, JSBuild
is a new Python library and a command-line utility that builds specified CommonJS modules and
packages by generating unobtrusive Javascript code. Documentation is available at [http://jsbuild.kodfabrik.com](https://web.archive.org/web/20110204144234/http://jsbuild.kodfabrik.com/)

Installation
------------
Please make sure that your system meets the requirements listed below:
 - Linux or any other Unix distribution, OS X as well (It probably works on Microsoft Windows, too, but I haven't tested it yet) 
 - Python 3+

To Install: 

  $ python3 setup.py install

Now you should be able to call jsbuild command which merges the Javascript files defined in the
specified manifest file. Optionally, you may run it on on your command-line passing no parameter to
test your installation, it should raise an output like the error message below:

  ERROR - Missing manifest path. More info with "-h" 

vim: tw=100
