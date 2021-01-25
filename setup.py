#!/usr/bin/env python
import setuptools
import os

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
     name='dte',  
     version='0.0.57',
     author="Marcelo V. Rozanti",
     author_email="mvrozanti@hotmail.com",
     description="Date Time Expressions",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/mvrozanti/dte",
     packages=setuptools.find_packages('dte'),
     install_requires=[
         'python-dateutil', 'ply'
         ],
     scripts=[
         'dte/dte',
         ],
     classifiers=[
         "Development Status :: 4 - Beta",
         "Topic :: Artistic Software",
         "Intended Audience :: Developers",
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: 3.7",
         "Programming Language :: Python :: 3.8",
         "Programming Language :: Python :: 3.9",
         "Programming Language :: Python :: 3 :: Only",
         ],
 )
