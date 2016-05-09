#!/usr/bin/env python

from setuptools import setup

setup(name='Greptile',
      version='0.9',
      description='Grep implementation with replace',
      author='Nicolas Cornette',
      author_email='nicolas.cornette@gmail.com',
      url='https://github.com/ncornette/greptile',
      packages=[],
      py_modules=['greptile'],
      entry_points={
          'console_scripts': [
              'greptile = greptile:main'
          ]
      }
      )
