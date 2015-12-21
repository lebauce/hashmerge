#!/usr/bin/env python

from setuptools import setup

setup(
    name='hashmerge',
    version='0.1',
    url='https://github.com/lebauce/hashmerge',
    author='Sylvain Baubeau',
    author_email='bob@glumol.com',
    description="Merges two arbitrarily deep hashes into a single hash.",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    py_modules=['hashmerge'],
    long_description="",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries'],
)
