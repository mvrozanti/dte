#!/usr/bin/env python
import setuptools
import os

with open('README.md', 'r') as fh:
    long_description = fh.read()

libdir = os.path.dirname(os.path.realpath(__file__))
requirements_path = libdir + '/requirements.txt'
install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
     name='dte',  
     version='0.0.4',
     author="Marcelo V. Rozanti",
     author_email="mvrozanti@hotmail.com",
     description="Date Time Expressions",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/mvrozanti/dte",
     packages=setuptools.find_packages(),
     install_requires=install_requires,
     scripts=[
         'dte/dte',
         ],
     classifiers=[
         "Development Status :: 4 - Beta",
         "Topic :: Artistic Software",
         "Intended Audience :: Developers",
         "Programming Language :: Python :: 3.4",
         "Programming Language :: Python :: 3.5",
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: 3 :: Only",
         ],
 )
