from os.path import splitext, basename
from jsbuild.logging import logger

FORMATS = {}
MODULES = {
  'js':['jsbuild.jsfile'],
  'json':['jsbuild.jsonindex'],
  'yaml':['jsbuild.yamlindex']
}

def load_ext_modules(ext):
  "Load the modules mapped with passed file extension"
  logger.debug('Loading modules mapped with specified extension "%s"'%ext)
  if not MODULES.__contains__(ext) or not MODULES[ext]:
    logger.error('No module names mapped with %s'%ext)

  modules = MODULES[ext]
  for filename in modules:
    __import__(filename)
    modules.pop(0)

def get_class_by_format(filename):
  "Find file extension of the passed filename and return mapped class mapped with that"
  logger.debug('Trying to get matching of %s'%basename(filename))
  ext = splitext(filename)[1][1:]
  if not FORMATS.__contains__(ext):
    try:
      logger.warning('Extension "%s" is not mapped to any class'%ext)
      load_ext_modules(ext)
    except:
      raise Exception('File with unknown format:',filename)
  return FORMATS[ext]
