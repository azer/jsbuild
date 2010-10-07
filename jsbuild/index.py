from functools import partial
from glob import glob
from itertools import chain
from jsbuild.dependency import Dependency
from jsbuild.logging import logger
from jsbuild.manifest import Manifest
from jsbuild.maps import get_class_by_format
from jsbuild import templates
import os.path
import re

class Index(Dependency):
  def __init__(self,*args,**kwargs):
    super(Index,self).__init__(*args,**kwargs)
    self._buffer_ = None
    self._manifest_ = None
    self._dependencies_ = None
    self.to_call = []

  @property
  def buffer(self):
    if not self._buffer_:
      self._buffer_ = self.read()
    return self._buffer_

  @property
  def content(self):

    root = self
    while root.index: root = root.index
    name = root.manifest.name

    content = '\n'.join(map(lambda dep: dep.content if not isinstance(dep,Index) or not dep.get_config('filename',False) else dep.put() or '', self.dependencies))

    if not self.index: 
      content = templates.jspackage%{ "name":name, "content":content }

    for flname in self.to_call:
      content = '%s\n%s'%(content,templates.jsmaincall%{ "index_name":self.manifest.name, "filename":flname})

    for rpl in self.get_config('replacements',[]):
      content = re.sub(rpl['pattern'],rpl['replacement']%self.get_config('dict',{}),content,flags=re.DOTALL)

    return content

  @property
  def dependencies(self):
    if self._dependencies_ == None:
      self.import_manifest()
    return self._dependencies_

  @property
  def manifest(self):
    if self._manifest_ == None:
      self._manifest_ = Manifest(self.parse())
    return self._manifest_

  def get_config(self,key,default=None):
    return self.manifest.build.__contains__(key) and self.manifest['build'][key] or default

  @property
  def source_dir(self):
    return os.path.normpath(os.path.join(self.working_dir,self.get_config('dir','')))

  def import_manifest(self):
    logger.debug('Importing manifest document')

    self._dependencies_ = []
    sdir = self.source_dir

    files = [ el for el in map(partial(lambda path: os.path.join(sdir,path)),self.get_config('files',[])) ]

    for depinfo in chain(*map(glob,files)):
      src = depinfo if not self.source_dir else depinfo[len(self.source_dir)+1:]
      dp = get_class_by_format(src)(index=self)
      dp.src = src
      self.dependencies.append(dp)

  def parse(self,content):
    raise Exception('Not Implemented')

  def put(self):
    filename = os.path.normpath(os.path.join(self.working_dir, self.get_config('filename')))
    with open('%s'%filename,'w') as fl:
      fl.write(self.content)
    logger.info('Writing %s OK'%filename)
