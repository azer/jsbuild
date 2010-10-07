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

  def testPathResolve(self):
    paths = re.findall('defineModule\("([^"]+)"',self.index.content)
    self.assertEqual( paths[0], 'corge.js')
    self.assertEqual( paths[1], 'foo/foo.js')
    self.assertEqual( paths[2], 'bar/bar.js')

  def testMainModule(self):
    self.index._manifest_['build']['main'] = 'corge.js'
    self.assertTrue( self.index.content.find( '._jsbuild_.getModuleByFilename("corge.js").call()' ) > -1 )

class LayoutTests(unittest.TestCase):
  def setUp(self):
    self.root = Index()
    self.root._dependencies_ = []

    self.corge = JSFile()
    self.corge.index = self.root
    self.corge.src = 'corge.js'
    setattr(self.corge, 'read', lambda *args: 'alert("corge says hello")')
    self.root.dependencies.append(self.corge)
    
    self.foo = Index()
    self.foo._dependencies_ = []
    self.foo.index = self.root
    self.root.dependencies.append(self.foo)

    self.qux = JSFile()
    self.qux.index = self.foo
    self.qux.src = 'qux.js'
    setattr(self.qux, 'read', lambda *args: 'alert("qux says hello")')
    self.foo.dependencies.append(self.qux)

    self.bar = Index()
    self.bar.index = self.root
    self.bar._dependencies_ = []
    self.root.dependencies.append(self.bar)

    self.quux = JSFile()
    self.quux.index = self.bar
    self.quux.src = 'quux.js'
    setattr(self.quux, 'read', lambda *args: 'alert("quux says hello")')
    self.bar.dependencies.append(self.quux)

    self.baz = Index()
    self.baz.index = self.bar
    self.baz._dependencies_ = []
    self.bar.dependencies.append(self.baz)

    self.spam = JSFile()
    self.spam.index = self.baz
    self.spam.src = 'grault/spam.js'
    setattr(self.spam, 'read', lambda *args: 'alert("spam says hello")')
    self.baz.dependencies.append(self.spam)

    self.eggs = JSFile()
    self.eggs.index = self.baz
    self.eggs.src = 'grault/eggs.js'
    setattr(self.eggs, 'read', lambda *args: 'alert("eggs says hello")')
    self.baz.dependencies.append(self.eggs)

  def testPackageTree(self):
    self.root.src = '/home/azer/newproject/manifest.json'
    self.root._manifest_ = Manifest({
      'name':'root',
      'build':{
         'dir':'lib',
         'filename':'/tmp/jsb_test_build',
         'main':'corge.js',
         'files':[
            'foo/manifest.json',
            'bar/manifest.json'
          ]
       }
    })

    self.foo.src = 'foo/manifest.json'
    self.foo._manifest_ = Manifest({
      'name':'foo',
      'build':{
        'main':'qux.js',
        'dir':'lib'
      }
    })

    self.bar.src = 'bar/manifest.json'
    self.bar._manifest_ = Manifest({
      'name':'bar',
      'build':{
         'main':'quux.js',
         'dir':'lib'
       }
    })

    self.baz.src = 'baz/manifest.json'
    self.baz._manifest_ = Manifest({
      'name':'baz',
      'build':{
         'main':'grault/eggs.js',
         'dir':'lib'
       }
    })

    module_paths = re.findall('defineModule\("([^"]+)"',self.root.content)
    self.assertEqual( module_paths[0], 'corge.js')
    self.assertEqual( module_paths[1], 'foo/qux.js')
    self.assertEqual( module_paths[2], 'bar/quux.js')
    self.assertEqual( module_paths[3], 'bar/baz/grault/spam.js')
    self.assertEqual( module_paths[4], 'bar/baz/grault/eggs.js')

    autorun_paths = re.findall('getModuleByFilename\("([^"]+)"\)\.call',self.root.content)
    self.assertEqual( len(autorun_paths), 4 )
    self.assertEqual( autorun_paths[0], 'foo/qux.js')
    self.assertEqual( autorun_paths[1], 'bar/baz/grault/eggs.js')    
    self.assertEqual( autorun_paths[2], 'bar/quux.js')
    self.assertEqual( autorun_paths[3], 'corge.js')

  def testGatheredTree(self):
    self.root.src = '/home/azer/newproject/build/manifests/root.json'
    self.root._manifest_ = Manifest({
      'name':'root',
      'build':{
         'dir':'../../src/lib',
         'filename':'/tmp/jsb_test_build',
         'main':'corge.js',
         'files':[
            '../../build/manifests/foo.json',
            '../../build/manifests/bar.json'
          ]
       }
    })

    self.foo.src = '../../build/manifests/foo.json'
    self.foo._manifest_ = Manifest({
      'name':'foo',
      'build':{
        'main':'qux.js',
        'dir':'../../src/lib/foo'
      }
    })

    self.bar.src = '../../build/manifests/bar.json'
    self.bar._manifest_ = Manifest({
      'name':'bar',
      'build':{
        'main':'quux.js',
        'dir':'../../src/lib/bar'
       }
    })

    self.baz.src = '../../../build/manifests/baz.json'
    self.baz._manifest_ = Manifest({
      'name':'baz',
      'build':{
        'main':'grault/eggs.js',
        'dir':'../../src/lib/bar/baz'
       }
    })

    paths = re.findall('defineModule\("([^"]+)"',self.root.content)
    self.assertEqual( paths[0], 'corge.js')
    self.assertEqual( paths[1], 'foo/qux.js')
    self.assertEqual( paths[2], 'bar/quux.js')
    self.assertEqual( paths[3], 'bar/baz/grault/spam.js')
    self.assertEqual( paths[4], 'bar/baz/grault/eggs.js')

    autorun_paths = re.findall('getModuleByFilename\("([^"]+)"\)\.call',self.root.content)
    self.assertEqual( len(autorun_paths), 4 )
    self.assertEqual( autorun_paths[0], 'foo/qux.js')
    self.assertEqual( autorun_paths[1], 'bar/baz/grault/eggs.js')    
    self.assertEqual( autorun_paths[2], 'bar/quux.js')
    self.assertEqual( autorun_paths[3], 'corge.js')

  def testSplittedManifests(self):
    self.root.src = '/home/azer/newproject/manifests/root.json'
    self.root._manifest_ = Manifest({
      'name':'root',
      'build':{
         'dir':'../src/lib',
         'filename':'/tmp/jsb_test_build',
         'main':'corge.js',
         'files':[
            '../manifests/foo.json',
            '../manifests/bar.json'
          ]
       }
    })

    self.foo.src = 'foo/manifest.json'
    self.foo._manifest_ = Manifest({
      'name':'foo',
      'build':{
        'filename':'/tmp/jsb_test_build_foo',
        'dir':'lib',
        'main':'qux.js'
      }
    })

    self.bar.src = 'bar/manifest.json'
    self.bar._manifest_ = Manifest({
      'name':'bar',
      'build':{
        'filename':'/tmp/jsb_test_build_bar',
        'dir':'lib',
        'main':'quux.js'
       }
    })

    self.baz.src = 'baz/manifest.json'
    self.baz._manifest_ = Manifest({
      'name':'baz',
      'build':{
         'dir':'lib',
         'main':'grault/eggs.js'
       }
    })

    paths = re.findall('defineModule\("([^"]+)"',self.root.content)
    self.assertEqual( len(paths), 1)
    self.assertEqual( paths[0], 'corge.js')

    autorun_path = re.findall('getModuleByFilename\("([^"]+)"\)\.call',self.root.content)
    self.assertEqual( len(autorun_path), 1 )
    self.assertEqual( autorun_path[0], 'corge.js')

    paths = re.findall('defineModule\("([^"]+)"',self.foo.content)
    self.assertEqual( len(paths), 1)
    self.assertEqual( paths[0], 'foo/qux.js')

    autorun_path = re.findall('getModuleByFilename\("([^"]+)"\)\.call',self.foo.content)
    self.assertEqual( len(autorun_path), 1 )
    self.assertEqual( autorun_path[0], 'foo/qux.js')

    paths = re.findall('defineModule\("([^"]+)"',self.bar.content)
    self.assertEqual( len(paths), 3)
    self.assertEqual( paths[0], 'bar/quux.js')
    self.assertEqual( paths[1], 'bar/baz/grault/spam.js')
    self.assertEqual( paths[2], 'bar/baz/grault/eggs.js')    

    autorun_paths = re.findall('getModuleByFilename\("([^"]+)"\)\.call',self.bar.content)
    self.assertEqual( len(autorun_paths), 2 )
    self.assertEqual( autorun_paths[0], 'bar/baz/grault/eggs.js')
    self.assertEqual( autorun_paths[1], 'bar/quux.js')
    
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

if __name__ == '__main__':
  unittest.main()
