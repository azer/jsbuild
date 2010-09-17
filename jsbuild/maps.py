from os.path import splitext
from jsbuild.jsfile import JSFile
from jsbuild.jsonindex import JSONIndex
from jsbuild.yamlindex import YAMLIndex

types = {
  'script':JSFile,
  'module':JSFile
}
formats = {
  'js':JSFile,
  'json':JSONIndex,
  'yaml':YAMLIndex
}

def get_class_by_format(filename):
  ext = splitext(filename)[1][1:]
  if not formats.__contains__(ext):
    raise Exception('File with unknown format:',filename)
  return formats[ext]
