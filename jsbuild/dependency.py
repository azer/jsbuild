from jsbuild.logging import logger
import os.path

class Dependency:
  def __init__(self,src=None,index=None):
    self._content_ = None
    self._src_ = None
    self._workingDir_ = ''
    self.filename = ''
    self.index = index

    if src: self.src = src

    logger.info('Initialized new dependency "%s"'%src)

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
    self.filename = os.path.basename(path)
    self._workingDir_ = os.path.dirname(path)

  @property
  def working_dir(self):
    return os.path.normpath(os.path.join(self.index.working_dir,self._workingDir_)) if self.index else self._workingDir_

  @working_dir.setter
  def working_dir(self,path):
    self._workingDir_ = path
  
  def read(self):
    path = os.path.normpath(os.path.join(self.working_dir,self.filename))
    logger.debug("Trying to read file '%s'"%path)
    with open(path) as fl:
      return fl.read()
