# Copyright (c) 2017  Pietro Albini <pietro@pietroalbini.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
=============
lektor-minify
=============

This plugin allows you to minify the build artifacts of your `Lektor`_ project
during the build process, without any additional tool. It currently supports
minifying HTML, CSS and JS files.

The plugin only minifies the files changed during the last build, avoiding
slowing down the build if your project consists of a lot of files. Internally
it uses the rcssmin and rjsmin libraries, and it's released under the MIT
license.

`Learn more about the plugin`_

.. _Lektor: https://www.getlektor.com
.. _Learn more about the plugin: https://github.com/pietroalbini/lektor-minify-assets
'''

# -*- coding: utf-8 -*-

import setuptools


setuptools.setup(
    name = "lektor-minify",
    version = "1.0.dev0",
    license = "MIT",

    author = "Pietro Albini",
    author_email = "pietro@pietroalbini.org",

    description = "Minify build artifacts during the Lektor build process",
    long_description = __doc__,

    packages = [
        "lektor_minify",
    ],

    install_requires  =  [
        "rcssmin",
        "rjsmin",
        "django_htmlmin",
    ],

    entry_points = {
        "lektor.plugins": [
            "minify = lektor_minify:MinifyPlugin",
        ]
    },

    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
