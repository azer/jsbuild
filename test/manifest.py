#!/usr/bin/python3
import unittest
import sys
sys.path.append('../')
sys.path.pop(0)
from jsbuild.manifest import Manifest

class TestManifest(unittest.TestCase):
  def setUp(self):
    self.manifest = Manifest()
    self.manifest._dict_ = {
      'foo':'bar',
      'spam':'eggs'
    }
    self.manifest.qux = '%(foo)s'
    self.manifest.quux = {
      "corge":"%(spam)s"
    }

  def testReplacement(self):
    self.assertEqual( self.manifest._dict_['foo'], 'bar' )
    self.assertEqual( self.manifest._dict_['spam'], 'eggs' )
    self.assertEqual( self.manifest.qux, 'bar' )
    self.assertEqual( self.manifest.quux.corge, 'eggs' )

if __name__ == '__main__':
  unittest.main()
