from jsbuild.logging import logger
import os.path

class Dependency:
  def __init__(self,src=None,index=None):
    self._content_ = None
    self._src_ = None
    self.index = index

    if src: self.src = src

    logger.info('Initialized new dependency "%s"'%src)

  @property
  def content(self):
    if not self._content_:
      self._content_ = self.read()
    return self._content_

  @property
  def filename(self):
    return os.path.basename(self.src)

  @property
  def src(self):
    return self._src_

  @src.setter
  def src(self,path):
    self._src_ = path

  @property
  def working_dir(self):
    return os.path.normpath(os.path.join(self.index.source_dir if self.index else '',os.path.dirname( self.src ) if self.src else ''))

  def read(self):
    path = os.path.normpath(os.path.join(self.index.source_dir if self.index else '',self.src))
    logger.debug("Trying to read file '%s'"%path)
    with open(path) as fl:
      return fl.read()
