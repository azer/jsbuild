#!/usr/bin/python3
import unittest
import sys
sys.path.append('../../')
sys.path.pop(0)

from jsbuild.index import Index
from jsbuild.jsonindex import JSONIndex
from jsbuild.jsfile import JSFile
from jsbuild.manifest import Manifest

class TestIndex(unittest.TestCase):
  def setUp(self):
    self.index = Index()
    self.index._manifest_ = Manifest({
      'name':'eggs',
      'version':'1.0',
      'build':{
        'dir':'lib',
        'filename':'foobar.js',
        'files':[
          '*.js',
          'foo/*.js',
          'bar/*.js'
         ]
      }
    })
    self.index.working_dir = '../templates/examples/basic'

  def testWorkingDir(self):
    self.assertEqual(self.index.working_dir, "../examples/basic")

  def testDependencyCount(self):
    import pdb
    self.assertEqual( len(self.index.dependencies), 3 )

  def testDependencyTypes(self):
    for dp in self.index.dependencies:
      self.assertTrue(str(dp.__class__).index("JSFile")>-1)

  def testDependencyContent(self):
    dps = self.index.dependencies
    self.assertEqual( dps[0].src, 'lib/corge.js' )
    self.assertEqual( dps[1].src, 'lib/foo/foo.js' )
    self.assertEqual( dps[2].src, 'lib/bar/bar.js' )

  def testWorkingDir(self):
    dps = self.index.dependencies
    self.assertEqual( dps[0].working_dir, '../templates/examples/basic/lib' )
    self.assertEqual( dps[1].working_dir, '../templates/examples/basic/lib/foo' )
    self.assertEqual( dps[2].working_dir, '../templates/examples/basic/lib/bar' )

class TestJSONIndex(unittest.TestCase):
  def setUp(self):
    self.index = JSONIndex()

  def testBasicManifest(self):
    self.index.src = '../templates/examples/basic/manifest.json'
    self.assertEqual(self.index.manifest.name,"example")
    self.assertEqual(self.index.manifest.version,"1.0")
    self.assertEqual(self.index.manifest.build.dir,'lib')

    self.index.import_manifest()

    dps = self.index.dependencies
    self.assertEqual( dps[0].working_dir, '../templates/examples/basic/lib' )
    self.assertEqual( dps[1].working_dir, '../templates/examples/basic/lib/foo' )
    self.assertEqual( dps[2].working_dir, '../templates/examples/basic/lib/bar' )
  
  def testNestedManifests(self):
    self.index.src = '../templates/examples/nested/manifest.json'
    self.index.import_manifest()
    self.assertEqual(self.index.manifest.name,"nested")
    self.assertEqual(self.index.manifest.version,"1.0")
    self.assertEqual(self.index.manifest.build.dir,'lib')

    dps = self.index.dependencies
    self.assertEqual( dps[0].working_dir, '../templates/examples/nested/lib' )
    self.assertEqual( dps[1].working_dir, '../templates/examples/nested/lib/foo' )
    self.assertEqual( len(dps[1].dependencies), 1)
    self.assertEqual( dps[1].dependencies[0].filename, 'foo.js')
    self.assertEqual( dps[1].dependencies[0].working_dir, '../templates/examples/nested/lib/foo/lib')
    self.assertEqual( dps[2].working_dir, '../templates/examples/nested/lib/bar' )

if __name__ == '__main__':
  unittest.main()
