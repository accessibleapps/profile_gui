from setuptools import setup

__version__ = "0.1"
__doc__ = """Quickly profile GUI applications"""

setup(
 name = "profile_gui",
 version = __version__,
 description = __doc__,
 py_modules = ['profile_gui'],
 install_requires = [
  'yappi',
  #'wxpython',
 ],
 zip_safe = False,
 classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Topic :: Software Development :: Libraries',
 ],
)
