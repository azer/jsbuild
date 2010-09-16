from dependency import Dependency
from functools import partial
from glob import glob
from manifest import Manifest
from itertools import chain
import re
import templates

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
    content = templates.jspackage%{ "name":self.manifest.name, "content":'\n'.join( map( lambda dep: jsmodule%{ "name":self.manifest.name, "filename":dep.src, 'content':dep.content }, self.dependencies) ) }

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
    from maps import get_class_by_format

    dir_spec = self.get_config('dir',None)
    if dir_spec: self.working_dir = self.working_dir + '/' + ( dirname(dir_spec) if re.findall('\/$',dir_spec) else dir_spec )

    files = [ el for el in map(partial(lambda index, path: (index.working_dir and index.working_dir+'/' or '')+path,self),self.get_config('files',[])) ]

    for depinfo in chain(*map(glob,files)):
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
