#!/usr/bin/python3
__author__ = "Azer Koçulu"
__copyright__ = "Copyright 2010, Kodfabrik"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "azer@kodfabrik.com"
__status__ = "Development"

from functools import partial
from jsmin import jsmin as minify
from os.path import splitext, dirname
from sys import argv as args
import re

from pdb import set_trace

with open('templates/package.js') as pkg_template:
  PACKAGE_TEMPLATE = pkg_template.read()

with open('templates/module.js') as mod_template:
  MODULE_TEMPLATE = mod_template.read()

TYPE_MAP = {}
FORMAT_MAP = {}

class Dependency:
  def __init__(self,src=None,index=None):
    self._content_ = None
    self._src_ = None
    self._workingDir_ = None
    self.index = index

    self.src = src

  @property
  def content(self):
    if not self._content_:
      self._content_ = self.read()
    return self._content_

  @property
  def src(self):
    return self._src_

  @src.setter
  def src(self,path):
    self._src_ = path
    self._workingDir_ = dirname(path)

  @property
  def working_dir(self):
    return '%s%s'%('%s/'%self.index.working_dir if self.index else '',self._workingDir_ or '')

  @working_dir.setter
  def working_dir(self,path):
    self._workingDir_ = path
  
  def read(self):
    try:
      with open('%s%s'%(self.index and self.index.working_dir+'/' or '',self.src)) as fl:
        return fl.read()
    except:
      set_trace()

class Index(Dependency):
  def __new__(cls,src,*args,**kwargs):
    ext = splitext(src)[1][1:]

    if not FORMAT_MAP.__contains__(ext):
      raise Exception('Unsupported Index Format: %s (%s)'%(ext,src))

    cls = FORMAT_MAP[ext]

    return super(Index,cls).__new__(cls,src,*args,**kwargs)

  def __init__(self,*args,**kwargs):
    super(Index,self).__init__(*args,**kwargs)
    self._dependencies_ = None
    self._manifest_ = None

  @property
  def content(self):
    content = '\n'.join( map( lambda dep: dep.content, self.dependencies) )

    for rpl in self.get_config('replacements',[]):
      content = re.sub(rpl['pattern'],rpl['replacement']%self.get_config('dict',{}),content,flags=re.DOTALL)

    return content

  @property
  def dependencies(self):
    if self._dependencies_ == None:
      self._dependencies_ = []
      self.import_manifest()
    return self._dependencies_

  @property
  def manifest(self):
    if not self._manifest_:
      self._manifest_ = self.parse(self.read())
    return self._manifest_ or {}

  def get_config(self,key,default=None):
    return self.manifest['build'].__contains__(key) and self.manifest['build'][key] or default

  def import_manifest(self):
    for depinfo in self.get_config('files',[]):
      src = None
      cls = None
      if isinstance(depinfo,str):
        src = depinfo
        cls = get_class_by_format(src)
      elif isinstance(depinfo,dict) and depinfo.__contains__('src'):
        src = depinfo['src']
        cls = TYPE_MAP[depinfo['type']] if depinfo.__contains__('type') else get_class_by_format(src)
      else:
        raise Exception('Could not resolve dependency info:',depinfo)

      self.dependencies.append(cls(src=src,index=self))

  def parse(self,content):
    raise Exception('Not Implemented')

  def put(self):
    with open('%s'%self.get_config('filename')%self.get_config('dict',{}),'w') as fl:
      fl.write(self.content)

TYPE_MAP['index'] = Index
TYPE_MAP['widget'] = Index
TYPE_MAP['application'] = Index

class JSFile(Dependency): pass

TYPE_MAP['script'] = JSFile
TYPE_MAP['module'] = JSFile
FORMAT_MAP['js'] = JSFile

class JSONIndex(Index):
  def __init__(self,*args,**kwargs):
    super(YAMLIndex,self).__init__(*args,**kwargs)
    self.lib = __import__('json')
    self.parse = self.lib.loads

FORMAT_MAP['json'] = JSONIndex

class YAMLIndex(Index):
  def __init__(self,*args,**kwargs):
    super(YAMLIndex,self).__init__(*args,**kwargs)
    self.lib = __import__('yaml')
    self.parse = self.lib.load

FORMAT_MAP['yaml'] = YAMLIndex

def get_class_by_format(filename):
  ext = splitext(filename)[1][1:]
  if not FORMAT_MAP.__contains__(ext):
    raise Exception('Unknown dependency type:',filename)
  return FORMAT_MAP[ext]

if __name__ == '__main__' and len(args)>1:
  src = args[1]
  ind = YAMLIndex(src)
  ind.working_dir = dirname(__file__) 
  ind.put()
