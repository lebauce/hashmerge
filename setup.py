#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hashmerge',
    version='0.2',
    url='https://github.com/lebauce/hashmerge',
    author='Sylvain Baubeau',
    author_email='bob@glumol.com',
    description="Merges two arbitrarily deep hashes into a single hash.",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    py_modules=['hashmerge'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries'],
)
