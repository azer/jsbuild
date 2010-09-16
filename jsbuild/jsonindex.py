from index import Index

class JSONIndex(Index):
  def parse(self):
    lib = __import__('json')
    return lib.loads(self.buffer)
