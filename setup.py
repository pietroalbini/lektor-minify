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
====================
lektor-minify-assets
====================

This plugin allows to minify the static assets of your Lektor website directly
from the build process, without any additional tool.

If you want to use it in your project, execute the command::

    $ lektor plugins add lektor-minify-assets

Then, you just need to build with the ``minify-assets`` flag::

    $ lektor build -f minify-assets

If you need to minify only CSS or JS though, you can either use the
``minify-css`` or ``minify-js`` flags to avoid minifying the other kind of asset.

`Learn more about the plugin`_

.. _Learn more about the plugin: https://github.com/pietroalbini/lektor-minify-assets
'''

# -*- coding: utf-8 -*-

import setuptools


setuptools.setup(
    name = "lektor-minify-assets",
    version = "1.0.dev0",
    license = "MIT",

    author = "Pietro Albini",
    author_email = "pietro@pietroalbini.org",

    description = "Minify static assets in a Lektor project",
    long_description = __doc__,

    py_modules = [
        "lektor_minify_assets",
    ],

    install_requires  =  [
        "rcssmin",
        "rjsmin",
    ],

    entry_points = {
        "lektor.plugins": [
            "minify-assets = lektor_minify_assets:MinifyAssetsPlugin",
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
