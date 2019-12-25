from os.path import abspath
from os.path import dirname
from os.path import join
from sys import path

# Allow the tests to find the source code.
project_root = abspath(dirname(dirname(__file__)))
src = join(project_root, "negotiator")
path.append(src)
