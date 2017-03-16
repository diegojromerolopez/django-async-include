# -*- coding: utf-8 -*-

#
# The MIT License (MIT)
#
# Copyright (c) 2015 by Diego J. Romero López <diegojromerolopez@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

data_files = []
for dirpath, dirnames, filenames in os.walk('.'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        continue
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name="django-async-include",
    version="0.2",
    author="Diego J. Romero López",
    author_email="diegojromerolopez@gmail.com",
    description="A simple application for Django to include (and fetch) asynchronous templates.",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        "pycryptodome",
        "jsonpickle"
    ],
    license="MIT",
    keywords="django template asynchronous template_tag",
    url='https://github.com/diegojromerolopez/django-async-include',
    packages=find_packages('.'),
    data_files=data_files,
    include_package_data=True,
)
