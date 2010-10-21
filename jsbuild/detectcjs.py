#!/usr/bin/python3
from functools import partial
import re

class Test:
  def __init__(self,exp=None,score=0):
    self.pattern = exp
    self.score = score

  @property
  def pattern(self):
    return self._pattern_

  @pattern.setter
  def pattern(self,exp):
    self._pattern_ = re.compile(exp) if exp else None

functions = re.compile('\(?(function[\s\w\_\$]*)\s*\([\s\w\$\,\/\*\_]*\)\{.*\}(\)\([\s\w\$\,\/\*\_]*\))?;?',re.DOTALL)

module_tests = (
  Test('exports\.([\w\$]+)\s*\=', 10),
  Test('\=\s*require\(', 10)
)

file_tests = (
  Test('(var|function|window\.)[\s]*(exports|require)[\s]*(\=|\()', 20),
  Test('(window|document)\.[\w\$]+', 5)
)

run_test = lambda source_code, test: test.score if test.pattern.search(source_code) else 0

def is_module(source_code):
  source_code = functions.sub('\\1',source_code)
  testrunner = partial(run_test,source_code)
  mod_score = sum(map(testrunner,module_tests))
  file_score = sum(map(testrunner,file_tests))
  return True if mod_score>file_score else bool(mod_score==file_score and mod_score)

if __name__ == '__main__':
  from sys import argv as args
  filename = args[1]
  with open(filename) as fl:
    print(is_module(fl.read()))
