#!/usr/bin/python3
import unittest
import sys
sys.path.append('../')
sys.path.pop(0)

from jsbuild.index import Index
from jsbuild.jsonindex import JSONIndex
from jsbuild.jsfile import JSFile

class TestIndex(unittest.TestCase):
  def setUp(self):
    self.index = JSONIndex()
    self.index.src = 'example/manifest.json'
    self.index.import_manifest()

  def testWorkingDir(self):
    self.assertEqual(self.index.working_dir, "example/lib")

  def testDependencyCount(self):
    self.assertEqual( len(self.index.dependencies), 6 )

  def testDependencyTypes(self):
    for dp in self.index.dependencies:
      self.assertTrue(str(dp.__class__).index("JSFile")>-1)

  def testDependencyContent(self):
    dps = self.index.dependencies
    self.assertEqual( dps[0].src, 'example/lib/corge.js' )
    self.assertEqual( dps[1].src, 'example/lib/foo/foo.js' )
    self.assertEqual( dps[2].src, 'example/lib/bar/bar.js' )
    self.assertEqual( dps[3].src, 'example/lib/bar/qux/eggs.js' )
    self.assertEqual( dps[4].src, 'example/lib/bar/quux/spam.js' )
    self.assertEqual( dps[5].src, 'example/lib/bar/quux/ham.js' )

class TestJSONIndex(unittest.TestCase):
  def setUp(self):
    self.index = JSONIndex()
    self.index.src = 'example/manifest.json'

  def testManifest(self):
    self.assertEqual(self.index.manifest.name,"example")
    self.assertEqual(self.index.manifest.version,"1.0")
    self.assertEqual(self.index.manifest.build.dir,'lib')

if __name__ == '__main__':
  unittest.main()
