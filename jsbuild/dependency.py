from os.path import dirname

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
    self._workingDir_ = path and dirname(path) or None

  @property
  def working_dir(self):
    return '%s%s'%(self.index.working_dir+'/' if self.index and self.index.working_dir else '',self._workingDir_ or '')

  @working_dir.setter
  def working_dir(self,path):
    self._workingDir_ = path
  
  def read(self):
    with open('%s%s'%(self.index.working_dir+'/' if self.index and self.index.working_dir else '',self.src)) as fl:
      return fl.read()
