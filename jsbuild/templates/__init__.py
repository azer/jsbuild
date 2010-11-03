import os.path
from jsbuild.logging import logger

DIR = os.path.dirname(__file__)
TEMPLATES = ['package.js','module.js','maincall.js','file.js']

for filename, template in map(lambda path: (os.path.normpath(os.path.join(DIR,path)),os.path.splitext(path)[0]), TEMPLATES):
  logger.debug('Trying to read the template named "%s" and located at "%s"'%(template,filename))
  with open(filename,encoding='utf-8') as source_code:
    globals()[template] = source_code.read()
