from jsbuild.dependency import Dependency
from jsbuild.maps import FORMATS
from jsbuild.logging import logger
from jsbuild import templates
import os.path

class JSFile(Dependency):
  @property
  def content(self):
    parents = []
    root = self
  
    while root.index:
      root = root.index
      parents.insert(0,root)

    logger.debug('Resolving module path of "%s"'%self.filename)
    wd = ''
    for index in parents:
      if not index.index: continue
      # print( 'Diving in to one more level', '[self.src]',self.src, '[self.working_dir]',self.working_dir, '[index.working_dir]', index.working_dir, '[index.source_dir]', index.source_dir )

      sdir = index.source_dir
      prelen = len(index.index.source_dir)
      suflen = len(index.get_config('dir',''))
      reldir = sdir[prelen+1 if prelen else 0: suflen*-1 if suflen and suflen<len(sdir)-prelen else None ]

      wd = os.path.normpath( os.path.join( wd, reldir) )
      
    filename = os.path.normpath( os.path.join(wd, self.src) )

    template = templates.jsmodule%{
      "name":root.manifest.name,
      "filename":filename,
      "content":super(JSFile,self).content
      }

    if self.index.get_config('main',None) == self.src:
      root.to_run.append( filename )
      #template = '%s\n%s'%(template,templates.jsautorun%{ 'index_name':root.manifest.name, 'filename':filename })

    return template

FORMATS['js'] = JSFile
logger.info('Associated JSFile class with "js" extension')
