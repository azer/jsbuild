#!/usr/bin/python3
import unittest
import sys
sys.path.append('../../')
sys.path.pop(0)

from jsbuild.dependency import Dependency

class TestDependency(unittest.TestCase):
  def setUp(self):
    self.dp = Dependency()
    self.dp.src = 'foobar/manifest.json'

  def testWorkingDir(self):
    self.assertEqual(self.dp.filename, "manifest.json")
    self.assertEqual(self.dp.working_dir, "foobar")
    self.dp.src = '../../foo/bar'
    self.assertEqual(self.dp.working_dir, '../../foo')
    self.assertEqual(self.dp.filename, "bar")
    self.dp.index = Dependency()
    self.assertEqual(self.dp.working_dir, '../../foo')
    self.dp.index.src = 'qux/quux/spam/eggs'
    self.assertEqual(self.dp.filename, "bar")
    self.assertEqual(self.dp.working_dir, 'qux/foo')

  def testRead(self):
    self.dp.filename = 'dependency.py'
    self.dp.working_dir = '../../test/lib'
    self.assertTrue(self.dp.read().find("self.assertTrue")>-1)

if __name__ == '__main__':
  unittest.main()
