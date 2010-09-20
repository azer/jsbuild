from jsbuild.dependency import Dependency
from jsbuild.templates import jsmodule
from jsbuild.maps import FORMATS
from jsbuild.logging import logger

class JSFile(Dependency):
  @property
  def content(self):
    root = self.index
    while root.index: root = root.index

    buffer = super(JSFile,self).content
    return jsmodule%{
      "name":root.manifest.name,
      "filename":self.src,
      "content":buffer
      }

FORMATS['js'] = JSFile
logger.info('Associated JSFile class with "js" extension')
