from distutils.core import setup

setup(name="pyometer",
      version="0.1",
      description="Python 3 metrics",
      license='MIT',
      author="Jake Ward",
      url='https://github.com/AthlosEducation/pyometer',
      packages=['pyometer', 'pyometer.metric', 'pyometer.reporter', 'pyometer.decorator'])
