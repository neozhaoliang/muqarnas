from setuptools import setup, find_packages


setup(name='muqarnas',
      version='0.0.1',
      description='A Python package for rendering beautiful geometry objects',
      author='Zhao Liang',
      author_email='mathzhaoliang@gmail.com',
      url='https://github.com/neozhaoliang/muqarnas',
      install_requires=['numpy', 'cairo'],
      packages=find_packages()
      )