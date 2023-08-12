from setuptools import setup
import os
# from freecad.workbench_starterkit.version import __version__
# name: this is the name of the distribution.
# Packages using the same name here cannot be installed together

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "freecad", "sprockets", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.sprockets',
      version=str(__version__),
      packages=['freecad',
                'freecad.sprockets'],
      maintainer="Iosiv42",
      maintainer_email="alkane_church@proton.me",
      url="https://github.com/Iosiv42/freecad.sprockets",
      description="FreeCAD module to create sprockets (aka. chainwheels).",
      install_requires=['numpy'], # should be satisfied by FreeCAD's system dependencies already
      include_package_data=True)
