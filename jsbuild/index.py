from functools import partial
from glob import glob
from itertools import chain
from jsbuild.dependency import Dependency
from jsbuild.logging import logger
from jsbuild.manifest import Manifest
from jsbuild import templates
import os.path
import re

class Index(Dependency):
  def __init__(self,*args,**kwargs):
    super(Index,self).__init__(*args,**kwargs)
    self._buffer_ = None
    self._manifest_ = None
    self.dependencies = []

  @property
  def buffer(self):
    if not self._buffer_:
      self._buffer_ = self.read()
    return self._buffer_

  @property
  def content(self):
    content = templates.jspackage%{ "name":self.manifest.name, "content":'\n'.join( map( lambda dep: templates.jsmodule%{ "name":self.manifest.name, "filename":dep.src, 'content':dep.content }, self.dependencies) ) }

    for rpl in self.get_config('replacements',[]):
      content = re.sub(rpl['pattern'],rpl['replacement']%self.get_config('dict',{}),content,flags=re.DOTALL)

    return content

  @property
  def manifest(self):
    if self._manifest_ == None:
      self._manifest_ = Manifest(self.parse())
    return self._manifest_

  def get_config(self,key,default=None):
    return self.manifest.build.__contains__(key) and self.manifest['build'][key] or default

  def import_manifest(self):
    logger.debug('Importing manifest document')
    from jsbuild.maps import get_class_by_format

    dir_spec = self.get_config('dir',None)
    if dir_spec: self.working_dir = (self.working_dir + '/' if self.working_dir else '') + ( dirname(dir_spec) if re.findall('\/$',dir_spec) else dir_spec )

    files = [ el for el in map(partial(lambda index, path: (index.working_dir and index.working_dir+'/' or '')+path,self),self.get_config('files',[])) ]

    for depinfo in chain(*map(glob,files)):
      src = None
      cls = None
      src = depinfo
      cls = get_class_by_format(src)
      if self.working_dir: src = src[len(self.working_dir)+1:]
      self.dependencies.append(cls(src=src,index=self))

  def parse(self,content):
    raise Exception('Not Implemented')

  def put(self):
    filename = self.get_config('filename') 
    with open('%s'%filename,'w') as fl:
      fl.write(self.content)
    logger.info('Writing %s OK'%filename)
