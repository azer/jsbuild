from jsbuild.dependency import Dependency
from jsbuild.templates import jsmodule
from jsbuild.maps import FORMATS
from jsbuild.logging import logger
import os.path

class JSFile(Dependency):
  @property
  def content(self):
    parents = []
    root = self

    while root.index:
      root = root.index
      parents.append(root)

    wdir = ''
    sdir = None
    for index in parents:
      prefix = index.index.get_config( 'dir', None ) if index.index else index.working_dir
      dirname = os.path.dirname( index.src ) if index.index else os.path.dirname( self.src )
      print('index.src:',index.src,'index.source_dir:',index.source_dir,'wdir:',wdir,'dirname:',dirname,'prefix:',prefix,'find:',dirname.find(prefix))
      wdir = os.path.join(wdir, dirname if not prefix or dirname.find(prefix) == -1 else dirname[len(prefix)+1:] )

    filename = os.path.normpath(os.path.join(wdir,self.filename))

    return jsmodule%{
      "name":root.manifest.name,
      "filename":filename,
      "content":super(JSFile,self).content
      }

FORMATS['js'] = JSFile
logger.info('Associated JSFile class with "js" extension')
