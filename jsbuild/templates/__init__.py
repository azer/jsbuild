from os.path import dirname

DIR = dirname(__file__)

with open('%s/package.js'%DIR) as pkg_template:
  jspackage = pkg_template.read()

with open('%s/module.js'%DIR) as mod_template:
  jsmodule = mod_template.read()

with open('%s/maincall.js'%DIR) as maincall_template:
  jsmaincall = maincall_template.read()
