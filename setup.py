from os.path import join
from setuptools import setup, find_packages


info = {}
execfile(join('deli', '__init__.py'), info)


setup(
    name = 'deli',
    version = info['__version__'],
    author = 'Tony S. Yu',
    author_email = 'tyu@enthought.com',
    maintainer = 'Tony S. Yu',
    maintainer_email = 'tyu@enthought.com',
    description = 'Interactive 2-dimensional plotting',
    include_package_data = True,
    install_requires = info['__requires__'],
    license = 'BSD',
    packages = find_packages(),
)
