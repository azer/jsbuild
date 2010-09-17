from jsbuild.index import Index

class YAMLIndex(Index):
  def parse(self):
    lib = __import__('yaml')
    lib.load(self.buffer)
