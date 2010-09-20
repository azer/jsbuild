from jsbuild.index import Index
from jsbuild.logging import logger
from jsbuild.maps import FORMATS
from os.path import basename

class JSONIndex(Index):
  def parse(self):
    logger.debug('Parsing %s'%self.src)
    lib = __import__('json')
    return lib.loads(self.buffer)

FORMATS['json'] = JSONIndex
logger.info('Associated "json" extension with JSONIndex class')
