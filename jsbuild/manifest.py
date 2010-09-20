from jsbuild.attrdict import AttrDict
from time import strftime

class Manifest(AttrDict):
  def __init__(self,*args,**kwargs):
    super(AttrDict, self).__init__(*args,**kwargs)
    self._buffer_ = None 
    self._parent_ = None

    if not self.__contains__('_dict_'):
      self['_dict_'] = {}
    
    self['_dict_']['timestamp'] = int(strftime("%Y%m%d%H%M"))

  def __getitem__(self,name):
    item = super(Manifest,self).__getitem__(name)

    if isinstance(item,Manifest) and not item._parent_:
      item._parent_ = self
    elif isinstance(item,str):
      root = self
      while root._parent_: root = root._parent_
      item = item%root._dict_

    return item
