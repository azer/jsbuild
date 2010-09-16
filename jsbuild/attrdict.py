from re import match

class AttrDict(dict):
  def __getattr__(self,name):
    superobj = super(AttrDict,self)
    getter = self.__getitem__ if self.__contains__(name) else superobj.__getattribute__
    return getter(name)

  def __getitem__(self,name):
    item = super(AttrDict,self).__getitem__(name)
    if not match('^_',name) and isinstance(item,dict):
      item = self.__class__(item)
      self.__setitem__(name,item)
    return item

  def __setattr__(self,name,value):
    if match('^_',name):
      super(AttrDict,self).__setattr__(name,value)
    else:
      self.__setitem__(name,value)
