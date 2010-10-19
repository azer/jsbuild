from jsbuild.dependency import Dependency
from jsbuild.maps import FORMATS
from jsbuild.logging import logger
from jsbuild import templates
import os.path
import re

class JSFile(Dependency):
  @property
  def content(self):
    parents = []
    root = self
  
    while root.index:
      root = root.index
      parents.insert(0,root)

    filename = os.path.normpath( os.path.join(self.index.path, self.src) )

    template = templates.jsmodule%{
      "name":root.manifest.name,
      "filename":filename,
      "content":super(JSFile,self).content
      }

    if self.index.get_config('main',None) == self.src and self.index.to_call.count( filename ) == 0:
      self.index.to_call.append( filename )
      logger.info('Added "%s" to "to call" list.'%filename)

    return template

FORMATS['js'] = JSFile
logger.info('Associated JSFile class with "js" extension')
