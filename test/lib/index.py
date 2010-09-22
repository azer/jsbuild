#!/usr/bin/python3
import unittest
import sys
import re
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
        'filename':'/tmp/jsb_test_build',
        'files':[
          '*.js',
          'foo/*.js',
          'bar/*.js'
         ]
      }
    })

    self.index.src = '../templates/examples/basic/manifest.json'

  def testDependencyCount(self):
    self.assertEqual( len(self.index.dependencies), 3 )

  def testDependencyTypes(self):
    for dp in self.index.dependencies:
      self.assertTrue(str(dp.__class__).index("JSFile")>-1)

  def testDependencyContent(self):
    dps = self.index.dependencies
    self.assertEqual( dps[0].src, 'corge.js' )
    self.assertEqual( dps[1].src, 'foo/foo.js' )
    self.assertEqual( dps[2].src, 'bar/bar.js' )

  def testWorkingDir(self):
    self.assertEqual(self.index.working_dir, "../templates/examples/basic")
    dps = self.index.dependencies
    self.assertEqual( dps[0].working_dir, '../templates/examples/basic/lib' )
    self.assertEqual( dps[1].working_dir, '../templates/examples/basic/lib/foo' )
    self.assertEqual( dps[2].working_dir, '../templates/examples/basic/lib/bar' )


  def testPathDefinitions(self):
    paths = re.findall('defineModule\("([^"]+)"',self.index.content)
    self.assertEqual( paths[0], 'corge.js')
    self.assertEqual( paths[1], 'foo/foo.js')
    self.assertEqual( paths[2], 'bar/bar.js')

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
    self.assertEqual(self.index.manifest.name,"example")
    self.assertEqual(self.index.manifest.version,"1.0")
    self.assertEqual(self.index.manifest.build.dir,'lib')

    dps = self.index.dependencies
    self.assertEqual( dps[0].working_dir, '../templates/examples/nested/lib' )
    self.assertEqual( dps[1].working_dir, '../templates/examples/nested/lib/foo' )
    self.assertEqual( len(dps[1].dependencies), 1)
    self.assertEqual( dps[1].dependencies[0].filename, 'foo.js')
    self.assertEqual( dps[1].dependencies[0].working_dir, '../templates/examples/nested/lib/foo')
    self.assertEqual( dps[2].working_dir, '../templates/examples/nested/lib/bar' )

  def testNestedPathDefinitions(self):
    self.index.src = '../templates/examples/nested/manifest.json'

    paths = re.findall('defineModule\("([^"]+)"',self.index.content)
    self.assertEqual( paths[0], 'corge.js')

    paths = re.findall('defineModule\("([^"]+)"',self.index.dependencies[1].content)
    self.assertEqual( paths[0], 'foo/foo.js')

    paths = re.findall('defineModule\("([^"]+)"',self.index.dependencies[2].content)
    self.assertEqual( paths[0], 'bar/bar.js')
    self.assertEqual( paths[1], 'bar/qux/eggs.js')
    self.assertEqual( paths[2], 'bar/quux/spam.js')
    self.assertEqual( paths[3], 'bar/quux/ham.js')

if __name__ == '__main__':
  unittest.main()
