from jsbuild.detectcjs import is_module
from jsbuild.dependency import Dependency
from jsbuild.maps import FORMATS
from jsbuild.logging import logger
from jsbuild import templates
import os.path
import re

class JSFile(Dependency):
  @property
  def content(self):
    source_code = super(JSFile,self).content
    template = templates.jsfile
    params = { "content":source_code }

    if is_module(source_code):
      parents = []
      root = self
      template = templates.jsmodule
  
      while root.index:
        root = root.index
        parents.insert(0,root)

      filename = os.path.normpath( os.path.join(self.index.path, self.src) )

      params['name'] = root.manifest.name
      params['filename'] = filename

      if self.index.get_config('main',None) == self.src and self.index.to_call.count( filename ) == 0:
        self.index.to_call.append( filename )
        logger.info('Added "%s" to "to call" list.'%filename)

    return template%params

FORMATS['js'] = JSFile
logger.info('Associated JSFile class with "js" extension')
