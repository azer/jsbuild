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

clean_backdir = lambda path: re.sub('^(\.\.\/?)+','',path)
count_backdir = lambda path: get_backdir(path).count('../')
has_backdir = lambda path: re.match('^\.\.',path) and True or False
join_path = lambda *args: os.path.normpath(os.path.join(*args))

def get_backdir(path):
  search = re.search('((?:\.\.\/)+)',path)
  return os.path.normpath(search.groups()[0]) if search else ''

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
      content = '%s\n%s'%(content,templates.jsmaincall%{ "index_name":root.manifest.name, "filename":flname})

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

  @property
  def path(self):
    logger.debug('Trying to find client-side path of "%s" (:working_dir %s :source_dir %s)'%(self.src,self.working_dir,self.source_dir))

    if not self.index: return ''

    parent = self.index
    parent_ref = get_backdir(self.src)

    while parent and has_backdir(parent_ref):
      print('parent.src: %s'%parent.src)
      parent_dir = join_path(os.path.dirname(parent.src) if parent.index else '',parent.get_config('dir',''))
      parent_dir_merged = join_path(clean_backdir(parent_dir),parent_ref)

      print('parent_ref: %s'%parent_ref,'parent_dir: %s'%parent_dir,'parent_dir_merged: %s'%parent_dir_merged)

      if len(parent_dir_merged)>0 and not parent_dir_merged=='.' and (not has_backdir(parent_dir_merged)): 
        print('breaking ',parent.src)
        break

      print('before change: %s'%os.path.join(parent_dir,parent_ref))
      parent_ref = join_path(parent_dir if parent.index and parent.index.index else clean_backdir(parent_dir),parent_ref)
      print('changed parent_ref: %s'%parent_ref)
      parent = parent.index
    
    print('done yo.',(parent.path,parent.src) if parent else None,self.src,(os.path.dirname(self.src)))
    path = join_path(parent.path if parent else '',clean_backdir(os.path.dirname(self.src)))

    return path if path!='.' else ''

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
