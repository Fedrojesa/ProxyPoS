from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES 
import os

packages, data_files = {},[]
root_dir = os.path.dirname(__file__)
if root_dir != "":
    os.chdir(root_dir)
proxypos_dir = "proxypos"

for dirpath, dirnames, filenames in os.walk(proxypos_dir):
    if "__init__.py" in filenames:
        if dirpath == proxypos_dir:
            packages[dirpath] = "."
        else:
            packages[dirpath.replace("/",".")] = "./"+dirpath
    elif filenames:
        data_files.append([dirpath,[os.path.join(dirpath,f) for f in filenames]])


for scheme in INSTALL_SCHEMES.values(): 
    scheme['data'] = scheme['purelib']

setup(name="proxypos",
      version="1.1.0",
      description = "",
      author ="",
      author_email = "",
      license="GPL",
      scripts=["proxypos/proxypos-server","proxypos/gtk-proxypos.py"],
      packages=packages,
      data_files = data_files,
)
